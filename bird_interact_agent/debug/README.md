# Always look at BIRD Interact README.md on the main repo
Follow instructions in README.md file for the latest changes: https://github.com/bird-bench/BIRD-Interact

To setup:
```
cd env
docker compose pull 
docker compose up -d
```

# Set up Data Locally

Make sure the data is available at: `.../bird_interact_agent/data/bird-interact-full` and `.../bird_interact_agent/data/bird-interact-lite`

# Run directly on VM

On host machine: `cd .../BIRD-Interact/env`: `docker compose exec bird_interact_eval bash`. This will log on the running container `bird_interact_eval`. Inside the container: `cd /app/bird_interact_agent`

**For lite version:**

`bash run_experiment-lite.sh`

**For full version:**

`bash run_experiment-full.sh`

# Debug the container with Debugpy

Update docker_compose.yaml to forward the port, under `bird_interact_eval` service:

```
ports:
  - "5678:5678"
```

## Install "debugy" on the running container

`Dockerfile.bird_interact_eval` is updated to make sure next build will include `debugpy`. This option you will need to rebuild the docker image. If this is your option, look at BIRD-Interact main repo, there is an instruction on rebuilding the image.

```
# Install debugy
RUN pip install debugpy
```

If you don't want to rebuild the image, but instead, you want to install the package directly to the running container.

```
docker compose exec bird_interact_eval bash
pip install debugpy
```
### Optionally, install debugpy from host

Use "docker ps" to find the id of the "bird_interact_eval" container
```
docker exec -it bird_interact_eval pip install debugpy
```

## Check debugy port forwarding

After you install `debugpy` package, you can restart the docker container. For example, `docker kill <container id>`, and then go to `env/` and `docker compose up -d`. You should see `0.0.0.0:5678->5678/tcp, :::5678->5678/tcp` under `PORT` on the console, when you do: `watch docker ps`.

## Create "debug" folder inside the running container

We need a folder that store the output for the debugging session. `Option 1` is to create the folder for the running container.

```
cd bird_interact_agent
docker compose exec bird_interact_eval bash
mkdir -p /app/outputs/single_runs/debug
```

`Option 2`: inside VSCode, when all containers are stopped, manually create the `single_runs/debug` folder.

## Create debugpy entry for VSCode launch.json 

Make sure `launch.json` has the following content:

```
{
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Attach to Docker (debugpy)",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        }
    ],
    "justMyCode": false
}
```

## Debug lite version with VSCode

On host console, start the debugger server for `lite` version, in `BIRD-Interact/env`:

```
 docker exec -it bird_interact_eval python -u -m debugpy --listen 0.0.0.0:5678 --wait-for-client ./bird_interact_agent/experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./bird_interact_agent/data/bird-interact-lite/bird_interact_data.jsonl --log_dir ./bird_interact_agent/outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_port 5432 --use_encoder_decoder --verbose
```

**Attach to Docker process from VSCode**

In oder to debug, attach to the debugging server on the container from VSCode by selecting `RUN AND DEBUG` left pannel - select the bug and triangle icon is the same.


Open `experiments/eval_react_bird_interact.py`, put the breakpoint at:

```
user_llm_provider = LLMProvider(
    provider=args.user_model_provider,
    model_id=args.user_model,
    token_counter=token_counter
)
```

Select `Attach to Docker (debugpy)` configuration defined in `launch.json` above. Click on the left Green triangle to start the debugger.

On VSCode, put the breakpoint inside `eval_react_bird_interact.py`, and start the bug icon on the left pannel, and select `Attach to docker (Debugy)`.

## Debug lite version with VSCode

On host console, start the debugger server for `lite` version, in `BIRD-Interact/env`:

```
 docker exec -it bird_interact_eval python -u -m debugpy --listen 0.0.0.0:5678 --wait-for-client ./bird_interact_agent/experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./bird_interact_agent/data/bird-interact-full/bird_interact_data.jsonl --log_dir ./bird_interact_agent/outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_host bird_interact_postgresql_full --db_port 5432 --use_encoder_decoder --verbose
```

**Attach to Docker process from VSCode**

In oder to debug, attach to the debugging server on the container from VSCode by selecting `RUN AND DEBUG` left pannel - select the bug and triangle icon is the same.


Open `experiments/eval_react_bird_interact.py`, put the breakpoint at:

```
user_llm_provider = LLMProvider(
    provider=args.user_model_provider,
    model_id=args.user_model,
    token_counter=token_counter
)
```

Select `Attach to Docker (debugpy)` configuration defined in `launch.json` above. Click on the left Green triangle to start the debugger.

## Note

if you stop the debugging session on VSCode UI, you need to restart the debugging server on the console before you can attach to it.


# Run directly from host

`For lite version`:

```
docker exec -it bird_interact_eval python -u ./bird_interact_agent/experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./bird_interact_agent/data/bird-interact-lite/bird_interact_data.jsonl --log_dir ./bird_interact_agent/outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_host bird_interact_postgresql --db_port 5432 --use_encoder_decoder --verbose
```


`For full version`:

```
docker exec -it bird_interact_eval python -u ./bird_interact_agent/experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./bird_interact_agent/data/bird-interact-full/bird_interact_data.jsonl --log_dir ./bird_interact_agent/outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_host bird_interact_postgresql_full --db_port 5432 --use_encoder_decoder --verbose
```

# Debug with local VSCode

## Setup local PostgreSQL

```
 1019  2025-10-24 07:53:31 sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm
 1020  2025-10-24 07:54:11 which psql
 1021  2025-10-24 07:54:38 sudo dnf -qy module disable postgresql
 1022  2025-10-24 07:55:21 docker exec -it bird_interact_postgresql psql --version
 1023  2025-10-24 07:55:48 sudo dnf install -y postgresql14
 1024  2025-10-24 07:56:28 psql --version
 1025  2025-10-24 07:56:43 psql -h bird_interact_postgresql -p 5432 -U root -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'postgres' AND pid <> pg_backend_pid();"

```

## Setup local conda env

```
conda create -n bird_interact python=3.12
conda activate bird_interact
cd .../bird_interact_agent
cd .../BIRD-Interact/env; pip install -r requirements_local.txt
```



