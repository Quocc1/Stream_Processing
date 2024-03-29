help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up              Bring up the Docker Compose environment with build"
	@echo "  down            Shut down the Docker Compose environment"
	@echo "  flink           Run the Flink job using Docker exec"
	@echo "  run             Run the whole project (shuts down, brings up, and run Flink job)"
	@echo "  grafana-ui      Open Grafana UI"
	@echo "  flink-ui        Open Flink UI"

up:
	docker compose up --build -d

down:
	docker compose down

flink:
	docker exec jobmanager ./bin/flink run --python ./code/main.py

run: down up flink

grafana-ui:
	explorer.exe http://localhost:3000

flink-ui:
	explorer.exe http://localhost:8081
