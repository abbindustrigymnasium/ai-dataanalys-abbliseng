function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
  }
  function deriviatesigmoid(y) {
      // return sigmoid(x) *(1 -sigmoid(x));
      return y * (1-y);
    }
  
  class NeuralNetwork {
    constructor(Numberinput, Numberhidden, Numberoutput) {
      this.Inputnodes = Numberinput;
      this.Hiddennodes = Numberhidden;
      this.OutputNodes = Numberoutput;
      //Skapar vikter för de oliak lagrerna och ger dem random värden.
      this.weights_ih = new Matrix(this.Hiddennodes, this.Inputnodes);
      this.weights_ho = new Matrix(this.OutputNodes, this.Hiddennodes);
      this.weights_ih.randomize();
      this.weights_ho.randomize();
  
      //Skapar bias för de oliak lagrerna och ger dem random värden.
      this.bias_h = new Matrix(this.Hiddennodes, 1);
      this.bias_o = new Matrix(this.OutputNodes, 1);
      this.bias_h.randomize();
      this.bias_o.randomize();
      this.learningrate=0.001;
    }
  
    //Det som skickas frammåt
    feedforward(input_array) {
      //Ta in värden i form av array, gör om dem till en endimensionell Matrix.
      let inputs = Matrix.fromArray(input_array);
      //Skapar en ny matrix från värdena och vikterna.
      let hidden = Matrix.multiply(this.weights_ih, inputs);
      //Lägger till Biasen
      hidden.add(this.bias_h);
      //Kör Aktiveringsmetoden (sigmoid i detta fall)
      hidden.map(sigmoid);
      //Gör samma en gång till fast för output layern
      let output = Matrix.multiply(this.weights_ho, hidden);
      output.add(this.bias_o);
      output.map(sigmoid);
      //Gör om det till en array och returnerar det.
      return output.toArray();
    }
  
    train(input_array, target_array) {
      //Ta in värden i form av array, gör om dem till en endimensionell Matrix.
      let inputs = Matrix.fromArray(input_array);
      //Skapar en ny matrix från värdena och vikterna.
      let hidden = Matrix.multiply(this.weights_ih, inputs);
      //Lägger till Biasen
      hidden.add(this.bias_h);
      //Kör Aktiveringsmetoden (sigmoid i detta fall)
      hidden.map(sigmoid);
      //Gör samma en gång till fast för output layern
      let outputs = Matrix.multiply(this.weights_ho, hidden);
      outputs.add(this.bias_o);
      outputs.map(sigmoid);
  
      let targets = Matrix.fromArray(target_array);
  
      //Räknar ut error, error = targets - outputs
      let output_errors = Matrix.subtract(targets, outputs);
      // let  gradient = outputs * (1-outputs);
      //Räknar ut gradient
      let gradients = Matrix.map(outputs,deriviatesigmoid);
      gradients.multiply(output_errors);
      gradients.multiply(this.learningrate);
      
      //Räknar ut deltas
      let hidden_T = Matrix.transpose(hidden);
      let weights_ho_deltas = Matrix.multiply(gradients,hidden_T);
     
      //Justera vikterna efter dess deltas
      this.weights_ho.add(weights_ho_deltas);
   //Justera bias efter dess deltas (gradients)
      this.bias_o.add(gradients);
  
  
  //Räknar ut erroret på hidden layer
      let weights_ho_transpose = Matrix.transpose(this.weights_ho);
      let hidden_errors = Matrix.multiply(weights_ho_transpose, output_errors);
      let hidden_gradient =Matrix.map(hidden,deriviatesigmoid);
      hidden_gradient.multiply(hidden_errors);
      hidden_gradient.multiply(this.learningrate);
  
      //Räknar ut hidden deltas
      let inputs_T = Matrix.transpose(inputs);
      let weights_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T);
  
      //Justera vikterna efter dess deltas
      this.weights_ih.add(weights_ih_deltas);
       //Justera bias efter dess deltas (gradients)
      this.bias_h.add(hidden_gradient);
  
      // outputs.print();
      // targets.print();
      // output_errors.print();
  
      // hidden_errors.print();
    }
  
    standarize(input_array){
      
  
      return outputarray;
    }
  
  }
  