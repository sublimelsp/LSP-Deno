// Tests for manually testing the `deno.client.test` command (the "▶ Run Test" / "Debug" code lenses).
//
// - "Run Test" runs only the test it belongs to and shows the output in the build output panel.
// - "Debug" does the same with `--inspect-wait`, so the test waits for a debugger to attach.
// - Lenses on steps and on `it(...)` run the whole enclosing top-level test.

// deno-lint-ignore-file no-import-prefix
import { assertEquals } from "jsr:@std/assert@1";
import { describe, it } from "jsr:@std/testing@1/bdd";

Deno.test("passes", () => {
  assertEquals(1 + 1, 2);
});

Deno.test("fails", () => {
  assertEquals(1 + 1, 3);
});

// The name contains regex special characters, which must be escaped in `--filter`.
Deno.test("adds (1 + 2) * 3 [regex chars]", () => {
  assertEquals((1 + 2) * 3, 9);
});

Deno.test(function namedFunction() {
  assertEquals("a".repeat(3), "aaa");
});

Deno.test({
  name: "object form",
  fn() {
    assertEquals([1, 2].length, 2);
  },
});

Deno.test("with steps", async (t) => {
  await t.step("first step", () => {
    assertEquals(1, 1);
  });
  await t.step("second step", () => {
    assertEquals(2, 2);
  });
});

describe("bdd suite", () => {
  it("works", () => {
    assertEquals(true, true);
  });
});
