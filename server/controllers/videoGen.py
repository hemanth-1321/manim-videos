import os
import uuid
from subprocess import run
from controllers.llm import llm_call
import shutil
import glob
import boto3
import random
from utils.db import db

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION")
)


async def generate_and_upload_video(prompt: str, user: str):
    print(user)

    video_id = None
    video = await db.video.create({
        "status": "PROCESSING",
        "prompt": prompt,
        "user": {
            "connect": {
                "id": user
            }
        }
    })
    video_id = video.id

    main_code = llm_call(prompt=prompt)
    uid = str(uuid.uuid4())
    filename = f"{uid}.py"
    output_file = f"{uid}.mp4"
    s3_key = f"videos/{uid}.mp4"

    with open(filename, "w") as f:
        f.write(main_code)

    run(["manim", filename, "MyScene"], check=True)
    render_dir = f"media/videos/{uid}"
    mp4_files = glob.glob(f"{render_dir}/**/MyScene.mp4", recursive=True)
    if not mp4_files:
        await db.video.update(
            where={"id": video_id},
            data={
                "status": "FAILED"
            }
        )
        return

    output_file = mp4_files[0]

    try:
        s3.upload_file(output_file, "manim.hemanth.buzz", s3_key)
        cloudfront_url = f"https://d3f2ks36ll5izf.cloudfront.net/{s3_key}"
        await db.video.update(
            where={"id": video_id},
            data={
                "url": cloudfront_url,
                "status": "CREATED"
            }
        )
        print(cloudfront_url)
    except Exception as e:
        await db.video.update(
            where={"id": video_id},
            data={
                "status": "FAILED"
            }
        )
        print(f"Upload failed: {e}")

    os.remove(filename)
    os.remove(output_file)

    media_folder = "media"
    if os.path.exists(media_folder):
        shutil.rmtree(media_folder)


async def get_all_videos():
    videos = await db.video.find_many(
        where={"status": "CREATED"},
        order={"created_at": "desc"}
    )
    random.shuffle(videos)
    return videos


async def get_Users_videos(user):
    print("userId", user)
    try:
        user_id = user.get("userId")
        videos = await db.video.find_many(
            where={"userId": user_id},
            order={"created_at": "desc"}
        )
        return videos
    except Exception as e:
        raise e
