import connect from "@/db/db";
import { NextRequest, NextResponse } from "next/server";
import amznProduct from "@/models/amazon";
import fkProduct from "@/models/flipkart";
import axios from "axios";

connect();

export async function POST(request: NextRequest) {
    try {
        const reqBody = await request.json();
        const { merchant, url, name } = reqBody;
        if (merchant == "FKRT") {
            if (url && name) {
                const product = await fkProduct.create({
                    productURL: url,
                    productName: name,
                });
                console.log(
                    `FKRT: \n\tADDED: ${product.productName} with URL: ${product.productURL}`,
                );
            }
        } else if (merchant == "AMZN") {
            if (url && name) {
                console.log(url);
                // const headers = {
                //     "User-Agent":
                //         "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                //     Accept: "text/html,*/*",
                //     "Accept-Language": "en-US,en;q=0.5",
                //     "Accept-Encoding": "gzip, deflate, br",
                //     "X-Requested-With": "XMLHttpRequest",
                //     DNT: "1",
                //     Connection: "keep-alive",
                //     Referer: "https://www.amazon.in/",
                //     "Sec-Fetch-Dest": "empty",
                //     "Sec-Fetch-Mode": "cors",
                //     "Sec-Fetch-Site": "same-origin",
                //     TE: "trailers",
                // };
                // await axios
                //     .get(url, { headers })
                //     .then((response: any) => {
                //         const redirectUrl = response.data;
                //         console.log(response);
                //         // Extract ASIN using regular expression
                //         const match = redirectUrl.match(/\/dp\/([A-Z0-9]{10})/);
                //         if (match) {
                //             const asin = match[1];
                //             console.log("ASIN extracted:", asin);
                //         } else {
                //             console.error("ASIN not found in redirect URL");
                //         }
                //     })
                //     .catch((error) => {
                //         console.error(
                //             "Error fetching redirect URL:",
                //             error.message,
                //         );
                //     });
                const product = await amznProduct.create({
                    productID: url,
                    productName: name,
                });
                console.log(
                    `AMZN: \n\tADDED: ${product.productName} with ASIN: ${product.productID}`,
                );
            }
        }
    } catch (error: any) {
        console.log(error.message);
    }
    return NextResponse.json({
        message: "request was recieved successfully",
    });
}
