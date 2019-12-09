
// Top level svg dimensions
const treeDimen = {
    "height": 1000,
    "width": 1000
};


const radius = treeDimen.width / 2;


// NOTE: Why 100 here? As in wheres the magic number from?
tree = d3.cluster()
    .size([2 * Math.PI, radius - 100]);


const root = tree(d3.hierarchy(data)
    .sort((a, b) => d3.ascending(a.data.name, b.data.name)));


// Select svg tree node and apply style
const svg = d3.select("#tree")
  .style("width", treeDimen.width + "px")
  .style("height", treeDimen.height + "px")


// .attr("fill", "none")
// Append inner g node, and apply style
const g = svg.append("g")
  .attr("transform", `translate(
      ${treeDimen.width / 2}, ${treeDimen.height / 2}
  )`);


// Create paths (a.k.a. the edge lines) and apply style
const link = g.selectAll("path")
.data(root.links())
.enter().append("path")
  .attr("class", "treeEdge")
  .attr("d", d3.linkRadial()
      .angle(d => d.x)
      .radius(d => d.y))

// Add the circular nodes
const node = g.append("g")
.selectAll("g")
.data(root.descendants().reverse())
.enter().append("g")
  .attr("class", "treeNode")
  .attr("transform", d => `
    rotate(${d.x * 180 / Math.PI - 90})
    translate(${d.y},0)
  `);

// NOTE: Chrome supports setting `r` from CSS, but FireFox does not.
// This is an SVG2 feaure, which is not fully supported yet.
node.append("circle")
      .attr("r", 2.5);
  
node.append("text")
  .attr("dy", "0.31em")
  .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
  .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
  .attr("transform", d => d.x >= Math.PI ? "rotate(180)" : null)
  .text(d => d.data.name)
.filter(d => d.children)
.clone(true).lower()


// svg.node().addEventListener("mousedown", function(event) {
//     console.log("Mousedown top g");
// });

// function update() { console.log("update"); }
// .on("start.update drag.update end.update", update)

function moveG(x,y) {
    g.attr("transform")
}

svg.call(d3.drag()
  .on("start", d => {
      // console.log("drag start");
  })
  .on("drag", d => {
      g.x = d3.event.x;
      g.y = d3.event.y;
  }) 
  .on("end", d => {
      // console.log("drag end");
  })
);



// QUES: Transform on `g` or `svg`? Consequences of each?
svg.call(d3.zoom()
  .on("zoom",  d => {
      // console.log(d);
      svg.attr("transform", d3.event.transform);
}));


// *****************************************************
// *****************************************************
// *****************************************************

const app = new Vue({
  el: '#vue-test',
  data: {
    message: 'Hello Vue!'
  }
});


class Tree {

    constructor() {
        this.height = 1000;
        this.width = 1000;


    }


}
