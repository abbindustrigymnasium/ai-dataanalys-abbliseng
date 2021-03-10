function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

class NeuralNetwork {
    constructor (input_nodes, hidden_nodes, output_nodes) {
        this.input_nodes = input_nodes;
        this.hidden_nodes = hidden_nodes;
        this.output_nodes = output_nodes;

        // Weights
        this.weights_ih = new Matrix(this.hidden_nodes, this.input_nodes);
        this.weights_ho = new Matrix(this.output_nodes, this.hidden_nodes);
        // Randomize the weights
        this.weights_ih.randomize();
        this.weights_ho.randomize();

        // Biases
        this.bias_h = new Matrix(this.hidden_nodes, 1);
        this.bias_h.randomize();
        this.bias_o = new Matrix(this.output_nodes, 1);
        this.bias_o.randomize();
    }

    feedforward(input_array) {
        // Turn input array into a matrix instance
        let inputs = Matrix.fromArray(input_array);

        let hidden = Matrix.multiply(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        hidden.map(sigmoid); // Activation function

        let output = Matrix.multiply(this.weights_ho, hidden);
        output.add(this.bias_o);
        output.map(sigmoid); // Activation function

        return output.toArray();
    }

    // Supervised learning
    train(inputs, targets) {
        let outputs = this.feedforward(inputs);

        outputs = Matrix.fromArray(outputs);
        targets = Matrix.fromArray(targets);

        let output_errors = Matrix.subtract(targets, outputs);

        let who_t = Matrix.transpose(this.weights_ho)
        let hidden_errors = Matrix.multiply(who_t, output_errors)

    }
}