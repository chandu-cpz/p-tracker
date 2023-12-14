import mongoose from "mongoose";
import { DB_NAME, MONGODB_URI } from "@/constants";

export default async function connect() {
    try {
        const conn = await mongoose.connect(`${MONGODB_URI}/${DB_NAME}`);
        console.log("MONGODB CONNECTED");
    } catch (error: any) {
        console.log(error.message);
    }
}
