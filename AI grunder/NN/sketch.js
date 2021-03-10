function setup() {

    let nn = new NeuralNetwork(2,2,1);
    let inputs = [1,0];
    let targets = [1];

    nn.train(inputs, targets);

    //let output = nn.feedforward(input);
    // console.log(output);
}