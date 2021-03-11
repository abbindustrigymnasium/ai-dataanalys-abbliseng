let nn;

let trainingdata = [
  { inputs: [0, 1], targets: [1] },
  { inputs: [0, 0], targets: [0] },
  { inputs: [1, 0], targets: [1] },
  { inputs: [1, 1], targets: [1] }
];
let testingdata = [
    [0,0],[0,1],[1,0],[1,1]
]
function setup() {
  //Skapar nätverket
  nn = new NeuralNetwork(2, 2, 1);
  
  //Skapar tränar det 100000 gånger
  for (let i = 0; i < 100000; i++) {
    data = random(trainingdata)
    nn.train(data.inputs, data.targets);
  }
  //Testar det med testdatavärdena vi har angett ovan
  for (let i = 0; i < testingdata.length; i++) {
   answer=  nn.feedforward(testingdata[i]);
   console.log(answer);
//   activatedAnswer= activationfunction(answer);
    // document.getElementById('logger').innerText+="\n"+testingdata[i][0]+" och "+testingdata[i][1]+" ger svaret "+ answer+" som enligt aktiveringsfunktionen är "+activatedAnswer;
    
  }//Samma som ovan fast manuelt
 // console.log( nn.feedforward([0,0])); 
 // console.log(nn.feedforward([0,1]));
 // console.log(nn.feedforward([1,0]));
 // console.log( nn.feedforward([1,1]));

}

// function activationfunction(input) {
//   //Easy step activation function
//   if (input>0.5) {
//     return 1
//   }
//   else
//   return 0
// }
// function draw() {}