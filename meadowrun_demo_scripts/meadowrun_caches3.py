import asyncio
import meadowrun


async def cache_pretrained_model_in_s3():
    return await meadowrun.run_command(
        "python backend/cache_in_s3.py --model_version mega_full --s3_bucket meadowrun-dallemini",
        meadowrun.AllocCloudInstance(1, 2, 80, "EC2"),
        meadowrun.Deployment.git_repo(
            "https://github.com/hrichardlee/dalle-playground",
            branch="s3cache",
            interpreter=meadowrun.PipRequirementsFile(
                "backend/requirements_for_caching.txt", "3.9"
            )
        )
    )


asyncio.run(cache_pretrained_model_in_s3())