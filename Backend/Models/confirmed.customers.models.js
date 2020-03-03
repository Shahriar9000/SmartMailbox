const mongoose = require("mongoose");

const Schema = mongoose.Schema; 

const goodCustomers = new Schema ( 
    {   name: {
            type: String
        },
        customer: {
            type: Number
        }
    }, 
    {
        versionKey: false // avoids adding the version key field
    }
);

const Customer = mongoose.model("Customer", goodCustomers, "Customer");

module.exports = Customer;
