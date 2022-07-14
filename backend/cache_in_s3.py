import argparse
import os

import boto3
import wandb

from consts import (DALLE_MODEL_MEGA, DALLE_MODEL_MEGA_FULL,
                            DALLE_MODEL_MINI, ModelSize)
from utils import parse_arg_dalle_version


def download_pretrained_model_and_cache_in_s3(model_version: ModelSize, s3_bucket: str, s3_bucket_region: str) -> None:
    wandb.init(anonymous="must")

    if model_version == ModelSize.MEGA_FULL:
        dalle_model = DALLE_MODEL_MEGA_FULL
    elif model_version == ModelSize.MEGA:
        dalle_model = DALLE_MODEL_MEGA
    else:
        dalle_model = DALLE_MODEL_MINI

    print(f"Will download and cache {dalle_model} in {s3_bucket}")

    tmp_dir = "dalle_pretrained_model"

    artifact = wandb.Api().artifact(dalle_model)
    artifact.download(tmp_dir)

    s3 = boto3.client("s3", region_name=s3_bucket_region)
    for file in os.listdir(tmp_dir):
        s3.upload_file(os.path.join(tmp_dir, file), s3_bucket, f"{model_version}/{file}")


def download_pretrained_model_from_s3(model_version: str, s3_bucket: str, s3_bucket_region: str) -> str:
    s3 = boto3.client("s3", region_name=s3_bucket_region)
    local_dir = os.path.join("/meadowrun/machine_cache", model_version)
    os.makedirs(local_dir, exist_ok=True)
    for file in s3.list_objects(Bucket=s3_bucket)["Contents"]:
        local_path = os.path.join("/meadowrun/machine_cache", file["Key"])
        if file["Key"].startswith(f"{model_version}/") and not os.path.exists(local_path):
            print(f"Downloading {file['Key']}")
            s3.download_file(s3_bucket, file["Key"], local_path)

    return local_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_version", type = parse_arg_dalle_version, required=True, help = "Mini, Mega, or Mega_full")
    parser.add_argument("--s3_bucket", required=True)
    parser.add_argument("--s3_bucket_region", required=True)
    args = parser.parse_args()
    
    download_pretrained_model_and_cache_in_s3(args.model_version, args.s3_bucket, args.s3_bucket_region)


if __name__ == "__main__":
    main()
