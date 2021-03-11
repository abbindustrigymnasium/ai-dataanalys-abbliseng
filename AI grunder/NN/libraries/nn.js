function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

function dsigmoid(y) {
    // return sigmoid(x) * (1 - sigmoid(x));
    return (y * (1 - y));
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

        this.learning_rate = 0.1;
    }

    check() {
        console.log("WEIGHTS")
        this.weights_ih.print()
        this.weights_ho.print()
        
        console.log("BIAS")
        this.bias_h.print()
        this.bias_o.print()
    }

    feedforward(input_array) {
        // Turn input array into a matrix instance
        let inputs = Matrix.fromArray(input_array);

        let hidden = Matrix.multiply(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        hidden.map(sigmoid); // Activation function

        let outputs = Matrix.multiply(this.weights_ho, hidden);
        outputs.add(this.bias_o);
        outputs.map(sigmoid); // Activation function

        return outputs.toArray();
    }

    // Supervised learning
    train(input_array, target_array) {
        // let outputs = this.feedforward(inputs);
        let inputs = Matrix.fromArray(input_array);
        let targets = Matrix.fromArray(target_array);
        
        let hidden = Matrix.multiply(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        Matrix.map(hidden, sigmoid);
        // hidden.map(sigmoid); // Activation function

        let outputs = Matrix.multiply(this.weights_ho, hidden);
        outputs.add(this.bias_o);
        Matrix.map(outputs, sigmoid)
        // outputs.map(sigmoid); // Activation function
        //
        let output_errors = Matrix.subtract(targets, outputs);


        // outputs = Matrix.fromArray(outputs);
        // Calculate gradients
        let gradients = Matrix.map(outputs, dsigmoid);
        // console.log(gradients)
        gradients.multiply(output_errors);
        // gradients.print()
        gradients.multiply(this.learning_rate);

        this.bias_o.add(gradients);
        // this.bias_o.print()

        // Calculate deltas
        let hidden_T = Matrix.transpose(hidden);
        let weight_ho_deltas = Matrix.multiply(gradients, hidden_T);

        this.weights_ho.add(weight_ho_deltas);
        this.weights_ho.print()

        // Hidden layer errors
        let who_t = Matrix.transpose(this.weights_ho);
        let hidden_errors = Matrix.multiply(who_t, output_errors);
        
        // HIDDEN LAYER
        let hidden_gradients = Matrix.map(hidden, dsigmoid);
        hidden_gradients.multiply(hidden_errors);
        hidden_gradients.multiply(this.learning_rate);

        this.bias_h.add(hidden_gradients);

        let inputs_T = Matrix.transpose(inputs);
        let weight_ih_deltas = Matrix.multiply(hidden_gradients, inputs_T)
        
        this.weights_ih.add(weight_ih_deltas);

        // this.check()
    }
}