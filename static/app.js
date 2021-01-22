const API_URL = "http://localhost:5000/api"

function cupcakeHTML(cupcakeJson){

    cupcakeCard = `
    <div class="card cupcake_card">
        <img class="card-img-top" src="..." alt="Card image cap">
        <div class="card-body">
            <p class="card-text">

                <p><strong>Flavor: </strong>${cupcake.flavor}</p>
                <p><strong>Size: </strong>${cupcake.size}</p>
                <p><strong>Rating: </strong>${cupcake.rating}</p>
        
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

async function cupcakeGetAll(){

    const response = await axios.get(`${API_URL}/cupcakes`);

    cupcakeJson = response.data.cupcakes;

    for (let cupcake of cupcakes){
        addCupcakeElement(cupcakeJson)
    };
};

async function cupcakePost(evt){
    evt.preventDefault();

    const flavor = $('#form-flavor').val();
    const rating = $('#form-rating').val();
    const size = $('#form-size').val();
    const image = $('#form-image').val();

    const response = await axios.post(`${API_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    cupcakeJson = response.data.cupcake;

    addCupcakeElement(cupcakeJson)

    $('#cupcake-form').trigger('reset');
};

async function cupcakeDelete(evt){

    evt.preventDefault();

    const $cupcake = $(evt.target).closest('#cupcake-card')
    const cupcakeId = $cupcake.attr('data-cupcake-id');

    await axios.delete(`${API_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();

}


$('#cupcake-form').on('submit', async function(evt){
    await cupcake_post(evt);
});

$('#cupcake-list').on('click', '.delete-cupcake', async function(evt){
    await cupcake_delete(evt);
});

$(cupcakeGetAll)