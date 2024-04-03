help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up              Spin up the Docker Compose environment"
	@echo "  down            Shut down the Docker Compose environment"
	@echo "  run             Run Flink job"
	@echo "  grafana-ui      Open Grafana UI"
	@echo "  flink-ui        Open Flink UI"

up:
	docker compose up -d

down:
	docker compose down

run: 
	docker exec jobmanager ./bin/flink run --python ./code/main.py

####################################################################################################################
# Monitoring
grafana-ui:
	explorer.exe http://localhost:3000

flink-ui:
	explorer.exe http://localhost:8081

# If you are using Linux, you may use this command instead
grafana-ui-linux:
	open http://localhost:3000

flink-ui-linux:
	open http://localhost:8081
