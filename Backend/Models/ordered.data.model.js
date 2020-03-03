const mongoose = require("mongoose");

const Schema = mongoose.Schema; 

const orderedItems = new Schema ( 
    {
        name: {
            type: String
        },
        time: {
            type: String
        },

        weight: {
            type: Number
        },

        barcode: {
            type: Number
        }
        
    }, 
    {
        versionKey: false // avoids adding the version key field
    }
);

const OrderedItems = mongoose.model("OrderedItems", orderedItems, "OrderedItems");

module.exports = OrderedItems;