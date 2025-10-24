
**run**

Follow instructions in README.md file for the latest changes: https://github.com/bird-bench/BIRD-Interact

```
cd env
docker compose pull 
docker compose up -d
```

**export port for docker_compose.yaml, under `bird_interact_eval` service**

```
ports:
  - "5678:5678"
```

**Check debugy port forwarding**

You should see `0.0.0.0:5678->5678/tcp, :::5678->5678/tcp` under `PORT` on the console, when you do: `watch docker ps`.

**create "debug" folder inside the running container**

```
cd bird_interact_agent
docker compose exec bird_interact_eval bash
mkdir -p /app/outputs/single_runs/debug
```

**install "debugy" on the running container**

`Dockerfile.bird_interact_eval` is updated to make sure next build will include `debugpy`:

```
# Install debugy
RUN pip install debugpy
```

or, if you don't want to rebuild the image:

```
docker compose exec bird_interact_eval bash
pip install debugpy
```

**Optionally, install with container id**

E.g., container_name=2686094332eb. **Note that this name is used in the command below, change accordingly**

Use "docker ps" to find the id of the "bird_interact_eval" container
```
docker exec -it 2686094332eb pip install debugpy
```

**set up data**

Make sure the data is available at: `.../bird_interact_agent/data/bird-interact-full` and `.../bird_interact_agent/data/bird-interact-lite`


**on host console, start the debugger server**

docker exec -it 2686094332eb python -u -m debugpy --listen 0.0.0.0:5678 --wait-for-client experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./data/bird-interact-lite/bird_interact_data.jsonl --log_dir ./outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_port 5432 --use_encoder_decoder --verbose

**Make sure VSCode launch.json has the following content**

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
                    "localRoot": "${workspaceFolder}/bird_interact_agent", # this is important to map
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
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

**Note**

if you stop the debugging session on VSCode UI, you need to restart the debugging server on the console before you can attach to it.


**Run directly from host**

```
docker exec -it 2686094332eb python -u experiments/eval_react_bird_interact.py --env bird_interact_sql --data_path ./data/bird-interact-lite/bird_interact_data.jsonl --log_dir ./outputs/single_runs/debug --max_turns 100 --agent_model openai/gpt-oss-120b --user_model openai/gpt-oss-120b --user_patience_budget 6 --agent_model_provider rits --user_model_provider rits --db_port 5432 --use_encoder_decoder --verbose
```
