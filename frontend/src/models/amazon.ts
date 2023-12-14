import mongoose from "mongoose";

const amznSchema = new mongoose.Schema(
    {
        productID: {
            type: String,
            required: true,
        },
        productName: {
            type: String,
            required: true,
        },
    },
    { timestamps: true },
);

const amznProduct =
    mongoose.models.amznProducts || mongoose.model("amznProducts", amznSchema);

export default amznProduct;
