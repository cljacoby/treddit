class App {

}

class Tree {

    constructor(data) {
        this.data = data;
        this.height = 1000;
        this.width = 1000;
        this.radius = this.radius / 2; 

        // TODO: Figure out what this value does
        this.fudge = 100;

        // Init d3 data structures
        this.cluster  = d3.cluster()
            .size([2 * Math.PI, radius - this.fudge]);

        // TODO: Define generic `name` visitor method. Able to set with respect to input data struture
        this.root = this.cluster(d3.hierarchy(data)
            .sort((a, b) => d3.ascending(a.data.name, b.data.name)));


    }


}
