const mongoose = require("mongoose");

const Schema = mongoose.Schema; 

const deliveredItems = new Schema (
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
       },
    },
    {
        versionKey: false
    }
);

const deliveredItem = mongoose.model("DeliveredItems", deliveredItems, "DeliveredItems");

module.exports = deliveredItem;