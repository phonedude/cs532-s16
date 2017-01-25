var width, height, color, svg, graph, linkGroups,
   nodefill = ["#8C564B", "#AEC7E8", "#2CA02C", "#1F77B4"], textsG,force,
   linksG, nodesG, k, tooltip, inOutExtent, circleRadius, node_drag, link;

var curLinksData = [], curNodesData = [], filter,
   layout, linkedByIndex = {},
   node, toggle = 0, text,
   sort, allData,
   padding = 1.5, // separation between circles
   radius = 25, curWhat = 16;


//most things were derived from    //https://flowingdata.com/2012/08/02/how-to-make-an-interactive-network-visualization/

//these are the color values and groupings I have mapped
// node groups:
//     normal: 0
// wsdl: 1
// diglib: 2
// odu: 3
//
// edge groups:
//     normal -> normal 0
// normal -> wsdl 1
// normal -> dlib 2
// normal -> odu 3
//
// wsdl -> normal 4
// wsdl -> wsdl 5
// wsdl -> dlib 7
// wsdl -> odu 6
//
//
// dlib -> normal 8
// dlib -> wsdl 9
// dlib -> dlib 10
// dlib -> odu 11
//
// odu -> normal 12
// odu -> wsdl 13
// odu -> dlib 14
// odu -> odu 15


function linkDist(l) {
   var ret;
   //make the link distances more dynamic i Kinda gave up here
   if (l.source.group == 0) {
      ret = 200;
   } else if (l.source.group == 1) {
      ret = 100;
   } else if (l.source.group == 2) {
      ret = 150;
   } else {
      ret = 175;
   }
   if (curWhat == 0) {
      ret = 200;
   }
   if (curWhat == 5) {
      ret = 200;
   }
   if (curWhat == 6) {
      ret = 200;
   }
   if (curWhat == 15) {
      ret = 200;
   }
   if (curWhat == 8) {
      ret = 200;
   }
   return ret;
}

function collide(node) {
   //got this from examples http://bl.ocks.org/mbostock/3231298#index.html
   var r = 2 * node.radius + 8,
      nx1 = node.x - r,
      nx2 = node.x + r,
      ny1 = node.y - r,
      ny2 = node.y + r;
   return function (quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== node)) {
         var x = node.x - quad.point.x,
            y = node.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = node.radius + quad.point.radius + padding;
         if (l < r) {
            l = (l - r) / l * .8;
            node.x -= x *= l;
            node.y -= y *= l;
            quad.point.x += x;
            quad.point.y += y;
         }
      }
      return x1 > nx2
         || x2 < nx1
         || y1 > ny2
         || y2 < ny1;
   };
}

function showDetails(d) {
   //show the detail about a node in the graph

   var content = '<p class="main">User Name: ' + d.name + '</span></p>';
   content += '<hr class="tooltip-hr">';
   content += '<p class="main"> Screen Name: ' + d.screenName + '</span></p>';
   content += '<hr class="tooltip-hr">';
   content += '<img src=' + d.imurl + ' alt="Stuff" style="width:100px;height:100px;">';
   tooltip.showTooltip(content, d3.event);
}


//begin not really used section
function mapNameToNode(nodes) {
   var map = d3.map();
   nodes.forEach(function (node) {
      map.set(node.screenName, node);
   });
   return map;
}


function buildIndex() {
   for (var i = 0; i < allData.nodes.length; i++) {
      linkedByIndex[i + "," + i] = 1;
   }
   allData.links.forEach(function (d) {
      linkedByIndex[d.source.index + "," + d.target.index] = 1;
   });
}

function neighboring(a, b) {
   return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index];
}
//end not really used section


//so when we redo things I can have the data already nice and tidy
function prepairData(data) {
   //the node radius is based on the sum of their in and out degree
   inOutExtent = d3.extent(data.nodes, function (node) {
      return node.indegree + node.outdegree;
   });

   circleRadius = d3.scale.sqrt()
      .range([3, 14]).domain(inOutExtent);

   data.nodes.forEach(function (n) {
      //where do we want to place our nodes
      n.x = Math.floor(Math.random() * width);
      n.y = Math.floor(Math.random() * height);
      n.radius = circleRadius(n.indegree + n.outdegree);
   });

   var nameNodeMap = mapNameToNode(data.nodes);
   data.links.forEach(function (l) {
      //point our links to the nodes that have position computed already
      var s = nameNodeMap.get(l.sname);
      var t = nameNodeMap.get(l.tname);
      l.sx = s.x;
      l.sy = s.y;
      l.tx = t.x;
      l.ty = t.y;
   });
   return data;
}

//begin copy pasta from http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
function dragstart(d, i) {
   force.stop(); // stops the force auto positioning before you start dragging
}
function dragmove(d, i) {
   d.px += d3.event.dx;
   d.py += d3.event.dy;
   d.x += d3.event.dx;
   d.y += d3.event.dy;
   tick();
}
function dragend(d, i) {
   // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
   d.fixed = true;
   tick();
   force.resume();
}
function releasenode(d) {
   d.fixed = false; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
   //force.resume();
}

//end copy pasta from http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/


function tick(e) {
   /*
      Do one iteraction of the force simulation
      consider our div elements size so we do not go outisde of it
    */
   var iw = $("#vis").innerWidth(), ih = $("#vis").innerHeight();
   link.attr("x1", function (d) {
         return d.source.x;
      })
      .attr("y1", function (d) {
         return d.source.y;
      })
      .attr("x2", function (d) {
         return d.target.x;
      })
      .attr("y2", function (d) {
         return d.target.y;
      });
   node
      .attr("cx", function (d) {
         return d.x = Math.max(6, Math.min(iw, d.x));
      })
      .attr("cy", function (d) {
         return d.y = Math.max(6, Math.min(ih, d.y));
      });


   node.each(collide);
}

function updateNodes() {
   /*
      when a user choses a new set of links to display we must redo the nodes
    */
   node = nodesG.selectAll("node")
      .data(curNodesData);
   node.enter().append("circle")
      .attr("class", "node")
      .attr("r", function (n) {
         return circleRadius(n.indegree + n.outdegree);
      })
      .style("fill", function (d) {
         return d3.rgb(nodefill[d.group]);
      })
      .style("stroke", function (d) {
         return d3.rgb(nodefill[d.group]).brighter().toString();
      })
      .on("mouseover", showDetails).on("mouseout", function () {
      tooltip.hideTooltip();
   }).on('dblclick', releasenode)
      .call(node_drag);
   //nuke them when done
   node.exit().remove();
}


function updateLinks() {
   /*
      when a user choses a new set of links to display we must redo the nodes
      this bad boy does the heavy lifting for us
      our nodes are set invisible based on their weight ie links to them
    */
   link = linksG.selectAll("link")
      .data(curLinksData);

   link.enter()
      .append("line")
      .attr("class", "link")
      .style("marker-end", "url(#to)");
   svg.selectAll("defs").remove();
   //since this graph is directed add some pointers to indicate the direction
   var def = svg.append("defs").selectAll("marker").data(["to"]);

   def.enter().append("marker")
      .attr("id", function (d) {
         return d;
      })
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 25)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
      .style("stroke", "#080808")
      .style("opacity", "1.0");
   def.exit().remove();
   link.exit().remove();
   node.filter(function (n) {
      return n.weight == 0;
   }).style("visibility", "hidden");

}


function update() {
   //on each change update the nodes
   force.links(curLinksData);
   force.nodes(curNodesData);
   force.start();
   updateNodes();
   updateLinks();

}


function makeVis(data) {
   /*
      called once do all things to make it so number one
      perpare the data
      get width height of the vis div element
    */
   allData = prepairData(data);
   width = $("#vis").width();
   height = $(window).innerHeight();
   //buildIndex();
   //build our link groups for our link displayer
   linkGroups = _.groupBy(allData.links, function (l) {
      return l.egroup
   });
   linkGroups[16] = _.filter(allData.links, function (l) {
      return l.tname == "WebSciDL";
   });
   linkGroups[17] = allData.links;
   curNodesData = allData.nodes;
   curLinksData = linkGroups[16];
   //do d3 things
   force = d3.layout.force();
   tooltip = Tooltip("vis-tooltip", 230);
   node_drag = d3.behavior.drag()
      .on("dragstart", dragstart)
      .on("drag", dragmove)
      .on("dragend", dragend);
   svg = d3.select("#vis").append("svg")
      .attr("width", width).attr("height", height);
   linksG = svg.append("g").attr("id", "links");
   nodesG = svg.append("g").attr("id", "nodes");
   textsG = svg.append("g").attr("id", "texts");
   force.size([width, height])
      .charge(-100).linkDistance(linkDist)
      .on("tick", tick);

   inOutExtent = d3.extent(data.nodes, function (node) {
      return node.indegree + node.outdegree;
   });

   circleRadius = d3.scale.sqrt()
      .range([3, 14]).domain(inOutExtent);
   update();
   buildIndex();
   $("#link_select").on("change", function (e) {
      //when our link_select value has changed update vis
      updateData($(this).val());
   });
}


function updateData(what) {
   //change our visualization to the link group selected
   curWhat = what;
   console.log("current what", what);
   curLinksData = linkGroups[what];
   node.each(function (n) {
      n.fixed = false;
   });
   link.remove();
   node.remove();
   update();
}

function resize() {
   //I wanted to take a stab at dynamic sizing of our vis
   width = $("#vis").width();
   height = $(window).innerHeight();
   svg.attr("width", width).attr("height", height);
   force.size([width, height]).resume();
}

//when the window resizes call resize
d3.select(window).on("resize", resize);

//load our data
d3.json("data/wsdlgraphData.json", function (error, data) {
   makeVis(data);
});
