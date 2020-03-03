const router = require("express").Router(); 

let OrderedItems = require("../models/ordered.data.model.js");
let DeliveredItems = require("../models/delivered.data.model.js");
let GoodCustomers = require("../models/confirmed.customers.models.js");

// app
router.get("/getOrders", (req, res) => {
    OrderedItems.find()
        .then(data => res.json(data))
        .catch(err => res.status(400).json("Error: " + err));
});

router.get("/getDelivered", (req, res) => {
    DeliveredItems.find()
        .then(data => res.json(data))
        .catch(err => res.status(400).json("Error: " + err));
});

// order by customer
router.post("/addOrders", (req, res) => {
    let name = req.body.name; 
    let time = req.body.time; 
    let weight = req.body.weight;
    let barcode = req.body.barcode;

    let newOrderedData = new OrderedItems({
        name,
        time,
        weight,
        barcode,
    }); 

    newOrderedData
        .save()
        .then(() => {
            res.status(200).json({data: "Data was added successfully"}); 
        })
        .catch(err => {
            res.status(400).send("New data was not successfully added"); 
        }); 
});

// order delivered to consumer
router.post("/addDelivered", (req, res) => {
    let name = req.body.name; 
    let time = req.body.time; 
    let weight = req.body.weight; 
    let barcode = req.body.barcode;

    let newDeliveredData = new DeliveredItems({
        name,
        time,
        weight,
        barcode
    });

    // Remove the delivered item from ordered (add to delivered)
    OrderedItems.deleteOne({ barcode: barcode }, function (err) {
        if (err) return handleError(err);
    });

    newDeliveredData
        .save()
        .then(() => {
            res.status(200).json({data: "Data was added successfully"}); 
        })
        .catch(err => {
            res.status(400).send("New data was not successfully added"); 
        }); 
});

// verify customer
router.get("/confirmCustomer", (req, res) => {
    GoodCustomers.find()
        .then(data => res.json(data))
        .catch(err => res.status(400).json("Error: " + err));
});

// after verified by customer
router.post("/recievedOrders", (req, res) => {
    DeliveredItems.remove({});
});

module.exports = router;