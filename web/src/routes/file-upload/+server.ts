import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const POST: RequestHandler = async ({ request }) => {
  const reader = request.body?.getReader();
  const content = reader?.read();

  if (content) {
    return json({
      success: true
    });
  }

  return json({
    success: false
  });
}