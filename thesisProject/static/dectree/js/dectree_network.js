alert(typeof(data))
var nodes = null;
var edges = null;
var network = null;
//alert(Array.isArray(db_edges))
//alert(abc);

function draw(){
	var nodes = db_nodes;
	var edges = db_edges;

	var mynetwork = document.getElementById('mynetwork');

	var container = document.getElementById('mynetwork');

	var data = {
		nodes: nodes,
		edges: edges
	};

	var options = {
		nodes: {
			fontColor: '#000000'
		},
		edges:{
			color: '#7C7C7C'
		},
		groups:{
			startNode: {
				shape: 'big box',
				color: '#24D017'
			},
			decision: {
				shape: 'box',
				color: '#57AFC9'
			},
			chance: {
				shape: 'circle',
				color: '#E73538'
			},
			leaf: {
				shape: 'text',
				color: '#5AA57D'
			}
		}
	}
	network = new vis.Network(container, data, options);
}
