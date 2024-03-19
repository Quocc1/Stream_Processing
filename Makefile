# Bring up the Docker Compose environment with build
up:
	docker compose up --build -d

# Shut down the Docker Compose environment
down:
	docker compose down

# Run the Flink job using Docker exec
flink:
	docker exec jobmanager ./bin/flink run --python ./code/main.py

# Run the Flink job
run: down up flink

# Open Grafana UI
grafana-ui:
	explorer.exe http://localhost:3000

# Open Flink UI
flink-ui:
	explorer.exe http://localhost:8081
