// Code for manually testing the `deno.client.showReferences` command (the "N references" / "N implementations" code
// lenses). Those lenses are disabled by default. Enable them in the LSP-Deno settings:
//
//   "settings": {
//     "deno.codeLens.implementations": true,
//     "deno.codeLens.references": true,
//     "deno.codeLens.referencesAllFunctions": true,
//   }
//
// Besides the lenses called out below, most classes, interfaces and members get a "N references" lens too.
//
// - A lens with a single location jumps straight to it.
// - A lens with multiple locations opens a picker that lists them.

// "2 implementations"
export interface Shape {
  area(): number;
}

// "1 implementation"
export interface Named {
  name: string;
}

export class Square implements Shape, Named {
  name = "square";
  constructor(readonly side: number) {}
  area(): number {
    return this.side * this.side;
  }
}

export class Circle implements Shape {
  constructor(readonly radius: number) {}
  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

// "3 references"
export function totalArea(shapes: Shape[]): number {
  return shapes.reduce((sum, shape) => sum + shape.area(), 0);
}

// "1 reference"
export function describe(shape: Named): string {
  return `${shape.name}: ${totalArea([])}`;
}

console.log(totalArea([new Square(2), new Circle(1)]));
console.log(totalArea([new Circle(2)]));
console.log(describe(new Square(3)));
