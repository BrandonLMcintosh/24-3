const API_URL = "http://localhost:5000/api"

function cupcakeHTML(cupcakeJson){

    cupcakeCard = `
    <div class="card cupcake-card" data-cupcake-id="${cupcakeJson.id}">
        <img class="card-img-top cupcake-card-image" src="${cupcakeJson.image}" alt="Card image cap">
        <div class="card-body">
            <p class="card-text">

                <p><strong>Flavor: </strong>${cupcakeJson.flavor}</p>
                <p><strong>Size: </strong>${cupcakeJson.size}</p>
                <p><strong>Rating: </strong>${cupcakeJson.rating}</p>

                <button class="delete-cupcake btn btn-danger">Delete</button>
        
            </p>
        </div>
    </div>
    `;

    return cupcakeCard;
};

function addCupcakeElement(cupcakeJson){
    const newCupcake = $(cupcakeHTML(cupcakeJson));
    $('#cupcake-list').append(newCupcake);
};

async function cupcakeAll(){

    const response = await axios.get(`${API_URL}/cupcakes`);

    cupcakes = response.data.cupcakes;

    for (let cupcakeJson of cupcakes){
        addCupcakeElement(cupcakeJson)
    };
};

async function cupcakePost(evt){
    evt.preventDefault();

    const flavor = $('#form-flavor').val();
    const rating = $('#form-rating').val();
    const size = $('#form-size').val();
    const image = $('#form-image').val() != "" ? $('#form-image').val() : null; 

    const response = await axios.post(`${API_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    cupcakeJson = response.data.post;

    addCupcakeElement(cupcakeJson)

    $('#cupcake-form').trigger('reset');
};

async function cupcakeDelete(evt){

    evt.preventDefault();

    const $cupcake = $(evt.target).closest('.cupcake-card')

    const cupcakeId = $cupcake.attr('data-cupcake-id');

    await axios.delete(`${API_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();

}


$('#cupcake-form').on('submit', async function(evt){
    evt.preventDefault()
    await cupcakePost(evt);
});

$('#cupcake-list').on('click', '.delete-cupcake', async function(evt){
    await cupcakeDelete(evt);
});

$(cupcakeAll)