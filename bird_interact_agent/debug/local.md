**setup postgreSQL client locally**

```
 1019  2025-10-24 07:53:31 sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm
 1020  2025-10-24 07:54:11 which psql
 1021  2025-10-24 07:54:38 sudo dnf -qy module disable postgresql
 1022  2025-10-24 07:55:21 docker exec -it bird_interact_postgresql psql --version
 1023  2025-10-24 07:55:48 sudo dnf install -y postgresql14
 1024  2025-10-24 07:56:28 psql --version
 1025  2025-10-24 07:56:43 psql -h bird_interact_postgresql -p 5432 -U root -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'postgres' AND pid <> pg_backend_pid();"

```

**setup local conda env**

`conda create -n bird_interact python=3.12`
`conda activate bird_interact`
`cd .../bird_interact_agent`
