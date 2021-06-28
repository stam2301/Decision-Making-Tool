
        var db_nodes = {{ db_nodes|safe }};
        var db_edges = {{ db_edges|safe }};
        var nodes = null;
        var edges = null;
        var network = null;

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
                    color: '#000000',
                    size: 10
                },
                edges:{
                    color: '#7C7C7C',
                },
                groups:{
                    startNode: {
				        shape: 'box',
                        color: '#F000FF',
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
                        shape: 'dot',
                        color: '#5AA57D'
                    },
                    research: {
                        shape: 'circle',
                        color: '#24D017'
                    }},
                    physics: {
                        enabled: true,
                        barnesHut: { 
                            gravitationalConstant: -1700,
                            centralGravity: 0.4,
                            springLength: 46,
                            springConstant: 0.032,
                            damping: 0.115}
                        
                        },
                    layout: {
                        hierarchical: {
                            direction: "LR"
                        }
                    }
                
            };
            network = new vis.Network(container, data, options);
            draw();
        }
