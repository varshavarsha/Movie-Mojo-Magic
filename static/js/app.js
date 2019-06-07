var submit = d3.select("#predict-btn");

submit.on("click", function () {

    // Prevent the page from refreshing
    d3.event.preventDefault();

    var gauge = d3.select("#gauge");
    gauge.html("");
    
    function validate_movie_form() {

        var title = document.getElementById('title').value;
        var runtime = document.getElementById('runtime').value;
        var genre = $('select#genre').val();
        var director = $('#director').val();
        var actor = $('select#actor').val();
        var poster = document.getElementById('poster').value;

        console.log(title);
        console.log(runtime);
        console.log(genre);
        console.log(director);
        console.log(actor);
        console.log(poster);

        if (title == "") {
            window.alert("Please enter the title.");
            title.focus();
            return false;
        }

        if (runtime == "") {
            window.alert("Please enter the runtime.");
            genre.focus();
            return false;
        }

        if (genre == "") {
            window.alert("Please enter the genre.");
            runtime.focus();
            return false;
        }

        if (director == "") {
            window.alert("Please enter the director.");
            director.focus();
            return false;
        }

        if (actor == "") {
            window.alert("Please enter the actor.");
            actor.focus();
            return false;
        }

        if (poster == "") {
            window.alert("Please upload the poster.");
            poster.focus();
            return false;
        }

        return true;

    }

    if (validate_movie_form()) {

        var form_data = new FormData($('#form_data')[0]);

        console.log(form_data);

        function postData() {
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: 'POST',
                    url: '/create_movie_prediction',
                    data: form_data,
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function (data) {
                        resolve(data)
                    },
                    error: function (error) {
                        reject(error)
                    },
                })
            })
        }
        postData()
            .then(response => {
                var prediction = response["Prediction"]
                console.log(prediction)
                createChart(prediction)
            })
            .catch(error => {
                console.log(error)
            })

        function createChart(prediction) {

            // Trig to calc meter point
            var degrees = 1 - prediction,
                radius = .5;
            var radians = degrees * Math.PI / 1;
            var x = radius * Math.cos(radians);
            var y = radius * Math.sin(radians);

            // Path: may have to change to create a better triangle
            var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
                pathX = String(x),
                space = ' ',
                pathY = String(y),
                pathEnd = ' Z';
            var path = mainPath.concat(pathX, space, pathY, pathEnd);

            var data = [{
                type: 'scatter',
                x: [0], y: [0],
                marker: { size: 28, color: '850000' },
                showlegend: false,
                name: 'prediction',
                text: prediction,
                hoverinfo: 'text+name'
            },
            {
                values: [50 / 2, 50 / 2, 50],
                rotation: 90,
                text: ['Hit', 'Not a Hit', ''],
                textinfo: 'text',
                textposition: 'inside',
                textfont: {
                    size: 18,
                },
                marker: {
                    colors: ['rgba(24, 169, 24, 1)', 'rgba(212, 22, 22, 1)', 'rgba(0,0,0,0)']
                },
                labels: ['1', '0', ''],
                hoverinfo: 'label',
                hole: .5,
                type: 'pie',
                showlegend: false
            }];

            var layout = {
                shapes: [{
                    type: 'path',
                    path: path,
                    fillcolor: '850000',
                    line: {
                        color: '850000'
                    }
                }],
                title: '<b>Movie Hit Predictor</b> <br> Predict a Movie with an IMDB Rating Above 7.5',
                height: 800,
                width: 800,
                xaxis: {
                    zeroline: false, showticklabels: false,
                    showgrid: false, range: [-1, 1]
                },
                yaxis: {
                    zeroline: false, showticklabels: false,
                    showgrid: false, range: [-1, 1]
                },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            };

            Plotly.newPlot('gauge', data, layout, { showSendToCloud: true });

        }
    
    }

    document.getElementById('title').value = "";
    document.getElementById('runtime').value = "";
    document.getElementById('poster').value = "";
    $('.selectpicker').val('').selectpicker('refresh');

})

