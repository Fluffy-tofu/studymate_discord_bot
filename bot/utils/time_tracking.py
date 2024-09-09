import discord
from datetime import datetime
from bot.db.database import SessionLocal
from bot.db.models import User, StudySession
from bot.embeds.stop_tracking_embed import stop_tracking_embed

class TimeTracker:
    @staticmethod
    async def start_tracking(interaction: discord.Interaction):
        try:
            user_id = interaction.user.id
            username = interaction.user.name
            now = datetime.now()

            with SessionLocal() as db_session:
                user = db_session.query(User).filter_by(discord_id=str(user_id)).first()
                if not user:
                    user = User(discord_id=str(user_id), username=username,
                                email='placeholder@test.com', password_hash='placeholder')
                    db_session.add(user)
                    db_session.flush()

                new_session = StudySession(discord_user_id=user.discord_id, start_time=now)
                db_session.add(new_session)
                db_session.commit()

            await interaction.response.send_message(f"Started tracking time for {interaction.user.mention}!", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

    @staticmethod
    async def stop_tracking(interaction: discord.Interaction):
        try:
            print('test')
            user_id = interaction.user.id
            now = datetime.now()

            with SessionLocal() as db_session:
                user = db_session.query(User).filter_by(discord_id=str(user_id)).first()

                if user:
                    study_session = db_session.query(StudySession).filter_by(discord_user_id=user.discord_id,
                                                                             end_time=None).order_by(StudySession.start_time.desc()).first()
                    if study_session:
                        study_session.end_time = now
                        elapsed_time = study_session.end_time - study_session.start_time
                        study_session.duration = elapsed_time.total_seconds() / 3600
                        db_session.commit()

                        elapsed_hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
                        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)

                        embed = stop_tracking_embed(start_time=study_session.start_time,
                                                    end_time=study_session.end_time,
                                                    elapsed_hours=int(elapsed_hours),
                                                    elapsed_minutes=int(elapsed_minutes),
                                                    elapsed_seconds=int(elapsed_seconds))

                        await interaction.response.send_message(embed=embed, ephemeral=False)
                    else:
                        await interaction.response.send_message("You don't have an active tracking session.", ephemeral=False)
                else:
                    await interaction.response.send_message("You haven't started any study sessions yet.", ephemeral=False)

        except Exception as e:
            await interaction.response.send_messge(f"An error occurred: {e}")
