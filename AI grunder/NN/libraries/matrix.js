class Matrix {

    //https://github.com/CodingTrain/website/blob/master/Courses/natureofcode/10.18-toy_neural_network/lib/matrix.js
  constructor(rows, cols) {
    this.rows = rows;
    this.cols = cols;
    this.data = []; //Tidiagre matrix.

    for (let i = 0; i < this.rows; i++) {
      this.data[i] = [];
      for (let j = 0; j < this.cols; j++) {
        this.data[i][j] = 0;
      }
    }
  }

  randomize() {
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
          
        this.data[i][j] += Math.floor(Math.random() * 2-1);
        // this.data[i][j] += Math.floor(Math.random() * 10);
      }
    }
  }

  add(n) {
    if (n instanceof Matrix) {
      for (let i = 0; i < this.rows; i++) {
        for (let j = 0; j < this.cols; j++) {
          this.data[i][j] += n.data[i][j];
        }
      }
    } else {
      for (let i = 0; i < this.rows; i++) {
        for (let j = 0; j < this.cols; j++) {
          this.data[i][j] += n;
        }
      }
    }
  }

  
  static subtract(a, b) {
    if (a.cols !== b.cols) {
      console.log("The row and columns must match.");
      return undefined;
    }

    let result = new Matrix(a.rows, a.cols);
    for (let i = 0; i < result.rows; i++) {
      for (let j = 0; j < result.cols; j++) {
        result.data[i][j] = a.data[i][j] - b.data[i][j];
      }
    }
    return result;
  }

  static transpose(matrix) {
    let result = new Matrix(matrix.cols, matrix.rows);
    for (let i = 0; i < matrix.rows; i++) {
      for (let j = 0; j < matrix.cols; j++) {
        result.data[j][i] = matrix.data[i][j];
      }
    }
    return result;
  }

  static multiply(a, b) {
    if (a.cols !== b.rows) {
      console.log("The row and columns must match.");
      return undefined;
    }

    let result = new Matrix(a.rows, b.cols);
    for (let i = 0; i < result.rows; i++) {
      for (let j = 0; j < result.cols; j++) {
        let sum = 0;
        for (let k = 0; k < b.rows; k++) {
          sum += a.data[i][k] * b.data[k][j];
        }
        result.data[i][j] = sum;
      }
    }
    return result;
  }

  print() {
    console.table(this.data);
  }

  multiply(n) {
    if (n instanceof Matrix) {
      for (let i = 0; i < this.rows; i++) {
        for (let j = 0; j < this.cols; j++) {
          this.data[i][j] *= n.data[i][j];
        }
      }
    } else {
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        this.data[i][j] *= n;
      }
    }
    }
  }

 static map(matrix,func) {
    //Applu a funcyion yo every element
    let result = new Matrix(matrix.rows,matrix.cols);
    
    for (let i = 0; i < matrix.rows; i++) {
      for (let j = 0; j < matrix.cols; j++) {
        let val = matrix.data[i][j];
        result.data[i][j] = func(val);
      }
    }
    return result;
  }

  map(func) {
    //Applu a funcyion yo every element
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        let val = this.data[i][j];
        this.data[i][j] = func(val);
      }
    }
  }

  static fromArray(arr){
      let m = new Matrix(arr.length,1);
      for (let i = 0; i < arr.length; i++) {
          m.data[i][0] = arr[i];
      }
      return m;
  }

  toArray(){
      let arr=[];
      for (let i = 0; i < this.rows; i++) {
          for (let j = 0; j < this.cols; j++) {
           arr.push(this.data[i][j]);            
          }     
      }
      return arr;
  }
}
