const BASE_URL = "http://localhost:5000/api";

function cupcakeHTML(cupcake){
    starRating = createStarRating(cupcake.rating)

    return `
        <div class="col-4 mb-4" data-cupcake-id="${cupcake.id}">
            <div class="card">
                <img src="${cupcake.image}" class="card-img-top">
                <div class="card-body text-center">
                    <h5 class="card-title">${cupcake.flavor}</h5>
                    <p class="card-text">${cupcake.size}</p>
                    <p class="card-text">${cupcake.rating}/10 - ${starRating}</p>
                    <button class="btn btn-danger btn-sm" id="delete-cupcake">Delete</button>
                </div>
            </div>
        </div>
    `;
}

function createStarRating(rating){
    let starRating = ``;
    let curRating = rating;

    for (let i = 0; i < 10; i++){
        if (curRating >= 1){
            starRating = starRating + '<span class="fa fa-star checked"></span>'
        } else if (curRating < 1 && curRating > 0){
            starRating = starRating + '<span class="fas fa-star-half-alt"></span>'
        }
        curRating -= 1;
    }

    return starRating;
}

async function showCupcakes(){
    const res = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcake of res.data.cupcakes){
        let newCupcake = $(cupcakeHTML(cupcake));
        $("#cupcakes-list").append(newCupcake);
    }
}

$("#create-cupcake-form").on("submit", async function (evt){
    evt.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    if (image === '') {
        image = "https://tinyurl.com/demo-cupcake"
    }

    const newCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(cupcakeHTML(newCupcakeRes.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#create-cupcake-form").trigger("reset")
})

$("#cupcakes-list").on("click", "#delete-cupcake", async function (evt) {
    evt.preventDefault();

    let $cupcake = $(evt.target).closest(".col-4");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
})

$(showCupcakes);