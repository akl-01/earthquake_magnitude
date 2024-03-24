import subprocess
import logging as log

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

class Application():
    def __init__(self) -> None:
        self.processes = {}
        self.python = "./.venv/bin/python"
    
    def docker_compose_up(self) -> None:
        logger.info("Run brokers")
        subprocess.run(["docker-compose", "--file", "configs/docker_compose.yaml", "up", "-d"])

    def docker_compose_stop(self) -> None:
        logger.info("Stop brokers")
        subprocess.run(["docker-compose", "--file", "configs/docker_compose.yaml", "down"])

    def start_processes(self) -> None:
        logger.info("Create processes")
        self.processes["real_data_producer"] = subprocess.Popen([self.python, "./app/backend/producers/real_time_producer.py"])
        self.processes["offline_producer"] = subprocess.Popen([self.python, "./app/backend/producers/offline_producer.py"])
        self.processes["data_processor_consumer"] = subprocess.Popen([self.python, "./app/backend/data_processor_consumer/data_processor_consumer.py"])
        self.processes["ml_consumer"] = subprocess.Popen([self.python, "./app/backend/ml_consumer/ml_consumer.py"])
        self.processes["visualization_sonsumer"] = subprocess.Popen([self.python, "-m", "streamlit", "run", 
                                                                     "./app/frontend/visualization_consumer/visualization_consumer.py"])

    def stop_processes(self) -> None:
        for name, process in self.processes.items():
            logger.info(f"Stopping {name} process")
            process.kill()
    
    def run(self) -> None:
        self.docker_compose_up()
        self.start_processes()
    
    def stop(self) -> None:
        self.stop_processes()
        self.docker_compose_stop()

if __name__ == "__main__":
    application = Application()

    try:
        logger.info("Run application")
        application.run()
        while True:
            continue
    except KeyboardInterrupt:
        logger.info("Stop application")
        application.stop()