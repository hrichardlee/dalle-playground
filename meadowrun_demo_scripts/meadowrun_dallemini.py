import asyncio
import meadowrun

async def run_dallemini():
    return await meadowrun.run_command(
        "python backend/app.py --port 8080 --model_version mini",
        meadowrun.AllocCloudInstance(
            logical_cpu_required=1,
            memory_gb_required=2,
            interruption_probability_threshold=80,
            cloud_provider="EC2",
            gpus_required=1,
            gpu_memory_required=4,
            flags_required="nvidia"
        ),
        meadowrun.Deployment.git_repo(
            "https://github.com/hrichardlee/dalle-playground",
            interpreter=meadowrun.PipRequirementsFile("backend/requirements.txt", "3.9")
        ),
        ports=8080
    )

asyncio.run(run_dallemini())