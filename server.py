import flwr as fl
from typing import List, Tuple
from flwr.common import Metrics

def weighted_average:
    accuracies = [num_examples * m["accuracy"]] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    return {"accuracy": sum(accuracies) / sum(examples)}

    strategy = fl.server.strategy.FedAvg(
        fraction_fit = 1.0,
        min_fit_clients = 2,
        min_available_clients = 3,
        evaluate_metrics_aggregation_fn = weighted_average
    )

if __name__ == "__main__":
    print("Starting Central Server...")
    fl.server.start_server(
        server_address = "0.0.0.0:8080",
        config = fl.server.ServerConfig(num_rounds=3),
        strategy=strategy,
    )
