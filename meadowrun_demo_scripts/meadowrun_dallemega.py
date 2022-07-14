import asyncio
import meadowrun

async def run_dallemega():
    return await meadowrun.run_command(
        "python backend/app.py --port 8080 --model_version mega_full --s3_bucket meadowrun-dallemini",
        meadowrun.AllocCloudInstance(1, 2, 80, "EC2", gpu_memory_required=12, flags_required="nvidia"),
        meadowrun.Deployment.git_repo(
            "https://github.com/hrichardlee/dalle-playground",
            branch="s3cache",
            interpreter=meadowrun.PipRequirementsFile("backend/requirements.txt", "3.9")
        ),
        ports=8080
    )

asyncio.run(run_dallemega())