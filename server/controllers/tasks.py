import os
import uuid
from subprocess import run
from controllers.llm import llm_call
import shutil
import glob
import asyncio
import boto3
from prisma import Prisma

db = Prisma()
s3 = boto3.client("s3")

async def generate_and_upload_video(prompt: str):
    await db.connect()
    
    if db.is_connected():
        print("[✅] Database connected successfully!")

    try:
        main_code = llm_call(prompt=prompt)
        uid = str(uuid.uuid4())
        filename = f"{uid}.py"
        output_file = f"{uid}.mp4"
        s3_key = f"videos/{uid}.mp4"

        # Write Manim code
        with open(filename, "w") as f:
            f.write(main_code)

        # Render video
        run(["manim", filename, "MyScene"], check=True)
        render_dir = f"media/videos/{uid}"
        mp4_files = glob.glob(f"{render_dir}/**/MyScene.mp4", recursive=True)
        if not mp4_files:
            print("[❌] MP4 not found after rendering.")
            return
        
        output_file = mp4_files[0] 
        print(f"[📁] Found rendered file: {output_file}")

        # Upload to S3
        try:
            s3.upload_file(output_file, "manim.hemanth.buzz", s3_key)
            cloudfront_url = f"https://d3f2ks36ll5izf.cloudfront.net/{s3_key}"
            db.video.create({
                "url":cloudfront_url
            })
            print("[✅] Upload successful!",cloudfront_url)
        except Exception as e:
            print(f"[❌] Upload failed: {e}")
            return  # Skip deletion if upload fails

        # Clean up only after successful upload
        os.remove(filename)
        os.remove(output_file)

        media_folder = "media"
        if os.path.exists(media_folder):
            shutil.rmtree(media_folder)

    finally:
        await db.disconnect()
        print("[ℹ️] Database disconnected.")

