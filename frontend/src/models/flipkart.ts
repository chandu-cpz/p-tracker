import mongoose, { Model } from "mongoose";

const fkSchema = new mongoose.Schema(
    {
        productURL: {
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

const fkProduct =
    mongoose.models.fkProducts || mongoose.model("fkProducts", fkSchema);
export default fkProduct;
