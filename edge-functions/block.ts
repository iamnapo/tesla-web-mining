import type { Config, EdgeFunction } from "@netlify/edge-functions";

const block: EdgeFunction = async (request, context) => {
	const userAgent = request.headers.get("user-agent");

	if (userAgent?.match(/Bytespider/)) {
		return new Response("Get out of here!", {
			status: 403,
			statusText: "Forbidden",
			headers: {
				"Content-Type": "text/plain",
			},
		});
	}

	return context.next();
};

export const config: Config = {
	path: "/*",
};

export default block;
