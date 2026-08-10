import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { parseVideoInput } from "./input";

describe("parseVideoInput", () => {
  it("accepts a three-image captioned input", () => {
    const result = parseVideoInput({
      title: "Drive Out: Keep Your Receipts",
      imagePaths: [
        "trial-assets/drive-out-poster.png",
        "trial-assets/drive-out-poster-2.png",
        "trial-assets/sample-shots.png",
      ],
      captions: [
        { text: "Track the work. Keep the proof.", startFrame: 0, endFrame: 90 },
      ],
      durationInFrames: 450,
    });

    assert.equal(result.imagePaths.length, 3);
    assert.equal(result.durationInFrames, 450);
  });

  it("rejects captions outside the declared duration", () => {
    assert.throws(
      () =>
        parseVideoInput({
        title: "Invalid",
        imagePaths: ["a.png", "b.png", "c.png"],
        captions: [{ text: "Too late", startFrame: 449, endFrame: 451 }],
        durationInFrames: 450,
        }),
      /Caption endFrame must be within the video duration/,
    );
  });
});
