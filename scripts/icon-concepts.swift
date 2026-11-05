// Cowboy State Eats icon concepts (2026-11-05), drawn in the shared Eats Ranked style (state-prompts/ICON-STYLE.md): one flat, level,
// centred food on sagebrush #3E4F3A (the landscape palette), no backing shape, no text or texture; no bucking horse and rider (the
// state's registered trademark), no University of Wyoming brown and gold, no hat or spurs. Food hexes: steak #9B3B2E, fat #F2E6CF,
// bone #FBF7EE, bun #D9A35B, sesame #F6E7C1, bison patty #5A2E1F, cheese #F0B93A, lettuce #8DBA5A, glass #DCE6E8, root beer #6B3A1F,
// ice cream #F4EBDD, cherry #B0172B, straw #C23B2E.
//   A  a T-bone steak from above: the meat inside its fat rim, the bone's T across it
//   B  a bison burger, side view: bun, patty, cheese, lettuce, a domed sesame bun
//   C  a root beer float at the soda fountain: a flared glass, a scoop of ice cream, a cherry and a straw
// Usage, from wy-eats/: swift scripts/icon-concepts.swift <out dir>   -> concept-{a,b,c}-1024.png
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let SAGE: UInt32 = 0x3E4F3A, STEAK: UInt32 = 0x9B3B2E, FAT: UInt32 = 0xF2E6CF, BONE: UInt32 = 0xFBF7EE, BUN: UInt32 = 0xD9A35B
let SESAME: UInt32 = 0xF6E7C1, PATTY: UInt32 = 0x5A2E1F, CHEESE: UInt32 = 0xF0B93A, LETTUCE: UInt32 = 0x8DBA5A, GLASS: UInt32 = 0xDCE6E8
let SODA: UInt32 = 0x6B3A1F, CREAM: UInt32 = 0xF4EBDD, CHERRY: UInt32 = 0xB0172B, STRAW: UInt32 = 0xC23B2E

func R(_ s: CGFloat, _ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, _ r: CGFloat) -> CGPath {
    CGPath(roundedRect: CGRect(x: x * s, y: y * s, width: w * s, height: h * s), cornerWidth: r * s, cornerHeight: r * s, transform: nil)
}

/// A: the T-bone. CoreGraphics y-up, s = canvas size.
func tbone(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(FAT)); c.addPath(R(s, 0.15, 0.32, 0.70, 0.38, 0.17)); c.fillPath()     // the fat rim
    c.setFillColor(rgb(STEAK)); c.addPath(R(s, 0.185, 0.35, 0.63, 0.32, 0.145)); c.fillPath() // the meat
    c.setFillColor(rgb(BONE))
    c.fill(CGRect(x: 0.47 * s, y: 0.35 * s, width: 0.06 * s, height: 0.27 * s))               // the T's stem
    c.addPath(R(s, 0.31, 0.58, 0.38, 0.06, 0.03)); c.fillPath()                                 // and its bar
}

/// B: a bison burger.
func burger(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(BUN)); c.addPath(R(s, 0.18, 0.30, 0.64, 0.09, 0.04)); c.fillPath()
    c.setFillColor(rgb(PATTY)); c.addPath(R(s, 0.15, 0.38, 0.70, 0.10, 0.05)); c.fillPath()
    c.setFillColor(rgb(CHEESE)); c.addPath(R(s, 0.20, 0.46, 0.60, 0.04, 0.02)); c.fillPath()
    c.setFillColor(rgb(LETTUCE)); c.addPath(R(s, 0.17, 0.49, 0.66, 0.04, 0.02)); c.fillPath()
    c.setFillColor(rgb(BUN)); c.addPath(R(s, 0.17, 0.52, 0.66, 0.18, 0.09)); c.fillPath()
    c.setFillColor(rgb(SESAME))
    for (x, y) in [(0.30, 0.62), (0.42, 0.65), (0.54, 0.63), (0.65, 0.60), (0.37, 0.57), (0.59, 0.56)] {
        c.fillEllipse(in: CGRect(x: CGFloat(x) * s, y: CGFloat(y) * s, width: 0.035 * s, height: 0.022 * s))
    }
}

/// C: a root beer float.
func float(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(STRAW))   // the straw first, behind the scoop
    c.saveGState(); c.translateBy(x: 0.58 * s, y: 0.66 * s); c.rotate(by: -0.45)
    c.fill(CGRect(x: 0, y: 0, width: 0.035 * s, height: 0.21 * s)); c.restoreGState()
    let glass = CGMutablePath()   // a flared fountain glass
    glass.move(to: CGPoint(x: 0.41 * s, y: 0.15 * s)); glass.addLine(to: CGPoint(x: 0.59 * s, y: 0.15 * s))
    glass.addLine(to: CGPoint(x: 0.67 * s, y: 0.68 * s)); glass.addLine(to: CGPoint(x: 0.33 * s, y: 0.68 * s)); glass.closeSubpath()
    c.setFillColor(rgb(GLASS)); c.addPath(glass); c.fillPath()
    let soda = CGMutablePath()
    soda.move(to: CGPoint(x: 0.425 * s, y: 0.18 * s)); soda.addLine(to: CGPoint(x: 0.575 * s, y: 0.18 * s))
    soda.addLine(to: CGPoint(x: 0.635 * s, y: 0.62 * s)); soda.addLine(to: CGPoint(x: 0.365 * s, y: 0.62 * s)); soda.closeSubpath()
    c.setFillColor(rgb(SODA)); c.addPath(soda); c.fillPath()
    c.setFillColor(rgb(CREAM)); c.fillEllipse(in: CGRect(x: 0.31 * s, y: 0.60 * s, width: 0.38 * s, height: 0.17 * s))
    c.setFillColor(rgb(CHERRY)); c.fillEllipse(in: CGRect(x: 0.46 * s, y: 0.75 * s, width: 0.08 * s, height: 0.08 * s))
}

func render(_ n: Int, _ path: String, _ draw: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(SAGE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    draw(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "playbook/brand"
render(1024, out + "/concept-a-1024.png", tbone)
render(1024, out + "/concept-b-1024.png", burger)
render(1024, out + "/concept-c-1024.png", float)
