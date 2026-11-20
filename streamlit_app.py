import json

import streamlit as st


st.set_page_config(
    page_title="입체도형 탐험실",
    page_icon="🧊",
    layout="wide",
)


COLORS = ["#4c83f6", "#f7a94b", "#37b99a", "#f16d79", "#a57af4", "#36abc7"]


def face(name, target, net, color):
    return {
        "name": name,
        "target": target,
        "net": [[x, y, 0] for x, y in net],
        "color": color,
    }


def box_faces(width, depth, height):
    x, y, z = width / 2, depth / 2, height / 2
    return [
        face(
            "앞면",
            [[-x, -y, -z], [x, -y, -z], [x, -y, z], [-x, -y, z]],
            [[-x, -z], [x, -z], [x, z], [-x, z]],
            COLORS[0],
        ),
        face(
            "오른쪽 면",
            [[x, -y, -z], [x, y, -z], [x, y, z], [x, -y, z]],
            [[x, -z], [x + depth, -z], [x + depth, z], [x, z]],
            COLORS[1],
        ),
        face(
            "뒷면",
            [[x, y, -z], [-x, y, -z], [-x, y, z], [x, y, z]],
            [[x + depth, -z], [x + depth + width, -z],
             [x + depth + width, z], [x + depth, z]],
            COLORS[2],
        ),
        face(
            "왼쪽 면",
            [[-x, -y, -z], [-x, -y, z], [-x, y, z], [-x, y, -z]],
            [[-x, -z], [-x, z], [-x - depth, z], [-x - depth, -z]],
            COLORS[3],
        ),
        face(
            "윗면",
            [[-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]],
            [[-x, z], [x, z], [x, z + depth], [-x, z + depth]],
            COLORS[4],
        ),
        face(
            "밑면",
            [[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z]],
            [[-x, -z], [x, -z], [x, -z - depth], [-x, -z - depth]],
            COLORS[5],
        ),
    ]


def triangular_prism_faces():
    a = [-1, -0.65]
    b = [1, -0.65]
    c = [0, 1.08]
    front_y, back_y = -0.9, 0.9
    ab = 2
    bc = ((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2) ** 0.5
    ca = bc
    return [
        face(
            "앞 삼각형",
            [[a[0], front_y, a[1]], [b[0], front_y, b[1]], [c[0], front_y, c[1]]],
            [[0, 0], [ab, 0], [ab / 2, -1.73]],
            COLORS[0],
        ),
        face(
            "첫째 옆면",
            [[a[0], front_y, a[1]], [b[0], front_y, b[1]],
             [b[0], back_y, b[1]], [a[0], back_y, a[1]]],
            [[0, 0], [ab, 0], [ab, 1.8], [0, 1.8]],
            COLORS[1],
        ),
        face(
            "둘째 옆면",
            [[b[0], front_y, b[1]], [c[0], front_y, c[1]],
             [c[0], back_y, c[1]], [b[0], back_y, b[1]]],
            [[ab, 0], [ab + bc, 0], [ab + bc, 1.8], [ab, 1.8]],
            COLORS[2],
        ),
        face(
            "셋째 옆면",
            [[c[0], front_y, c[1]], [a[0], front_y, a[1]],
             [a[0], back_y, a[1]], [c[0], back_y, c[1]]],
            [[ab + bc, 0], [ab + bc + ca, 0],
             [ab + bc + ca, 1.8], [ab + bc, 1.8]],
            COLORS[3],
        ),
        face(
            "뒤 삼각형",
            [[a[0], back_y, a[1]], [b[0], back_y, b[1]], [c[0], back_y, c[1]]],
            [[0, 1.8], [ab, 1.8], [ab / 2, 3.53]],
            COLORS[4],
        ),
    ]


def square_pyramid_faces():
    side_height = (1 + (1.35 + 0.7) ** 2) ** 0.5
    base = [
        [-1, -1, -0.7],
        [1, -1, -0.7],
        [1, 1, -0.7],
        [-1, 1, -0.7],
    ]
    apex = [0, 0, 1.35]
    return [
        face(
            "밑면",
            base,
            [[-1, -1], [1, -1], [1, 1], [-1, 1]],
            COLORS[0],
        ),
        face(
            "앞쪽 옆면",
            [base[0], base[1], apex],
            [[-1, -1], [1, -1], [0, -1 - side_height]],
            COLORS[1],
        ),
        face(
            "오른쪽 옆면",
            [base[1], base[2], apex],
            [[1, -1], [1, 1], [1 + side_height, 0]],
            COLORS[2],
        ),
        face(
            "뒤쪽 옆면",
            [base[2], base[3], apex],
            [[1, 1], [-1, 1], [0, 1 + side_height]],
            COLORS[3],
        ),
        face(
            "왼쪽 옆면",
            [base[3], base[0], apex],
            [[-1, 1], [-1, -1], [-1 - side_height, 0]],
            COLORS[4],
        ),
    ]


SHAPES = {
    "정육면체": {
        "description": "정사각형인 면 6개가 모여 모든 모서리의 길이가 같은 도형이에요.",
        "faces": box_faces(2, 2, 2),
        "fact": "면 6개 · 모서리 12개 · 꼭짓점 8개",
    },
    "직육면체": {
        "description": "직사각형인 면 6개가 모여 상자처럼 생긴 도형이에요.",
        "faces": box_faces(2.6, 1.8, 1.5),
        "fact": "면 6개 · 모서리 12개 · 꼭짓점 8개",
    },
    "삼각기둥": {
        "description": "삼각형인 밑면 2개와 직사각형인 옆면 3개로 이루어져요.",
        "faces": triangular_prism_faces(),
        "fact": "면 5개 · 모서리 9개 · 꼭짓점 6개",
    },
    "사각뿔": {
        "description": "사각형인 밑면 하나와 한 꼭짓점에 모이는 삼각형 옆면 4개가 있어요.",
        "faces": square_pyramid_faces(),
        "fact": "면 5개 · 모서리 8개 · 꼭짓점 5개",
    },
    "원기둥": {
        "description": "직사각형 옆면을 둥글게 말고 위·아래 원을 붙여 만들어요.",
        "faces": [],
        "geometry": {"type": "cylinder", "radius": 1, "height": 2.4},
        "fact": "면 3개 (곡면 1·원 2) · 모서리 2개 · 꼭짓점 0개",
    },
    "원뿔": {
        "description": "부채꼴 옆면을 말고 원 모양 밑면을 붙여 만들어요.",
        "faces": [],
        "geometry": {"type": "cone", "radius": 1, "slant": 2.6, "height": 2.4},
        "fact": "면 2개 (곡면 1·원 1) · 모서리 1개 · 꼭짓점 1개",
    },
}

SHAPE_NAMES = list(SHAPES)
POLYHEDRON_NAMES = [name for name in SHAPE_NAMES if not SHAPES[name].get("geometry")]
PROBLEMS = {
    "문제 A": "정육면체",
    "문제 B": "삼각기둥",
    "문제 C": "사각뿔",
    "문제 D": "직육면체",
}


def render_viewer(shape_name, base_face, mode, folded_reveal=True, fault="", fixed=False):
    shape_json = json.dumps(SHAPES[shape_name]["faces"], ensure_ascii=False)
    options_json = json.dumps(
        {
            "shapeName": shape_name,
            "baseFace": base_face,
            "mode": mode,
            "geometry": SHAPES[shape_name].get("geometry"),
            "foldedReveal": folded_reveal,
            "fault": fault,
            "fixed": fixed,
        },
        ensure_ascii=False,
    )
    template = r"""
    <div class="viewer">
      <div class="view-controls">
        <div class="control-group">
          <button id="topView">위에서 보기</button>
          <button id="frontView">정면 보기</button>
          <button id="resetView">시점 초기화</button>
        </div>
        <div class="control-group">
          <button id="foldPrev">이전 단계</button>
          <button id="foldNext" class="primary">다음 면 접기</button>
          <button id="foldAuto">전체 재생</button>
          <button id="unfold">처음부터</button>
        </div>
      </div>
      <div class="panels">
        <section class="panel" id="solidPanel">
          <div class="panel-heading"><span>입체도형</span><small>마우스로 끌어 360° 회전</small></div>
          <canvas id="solidCanvas" width="900" height="600"></canvas>
          <div class="panel-note" id="solidNote"></div>
        </section>
        <section class="panel">
          <div class="panel-heading"><span>전개도</span><small>마우스로 끌어 360° 회전</small></div>
          <canvas id="netCanvas" width="900" height="600"></canvas>
          <div class="panel-note" id="netNote"></div>
        </section>
      </div>
    </div>
    <style>
      * { box-sizing: border-box; }
      body { margin: 0; font-family: sans-serif; color: #23304a; }
      .viewer { background: #f7f9fd; border: 1px solid #e6ebf4; border-radius: 18px; padding: 14px; }
      .view-controls { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; margin-bottom: 12px; }
      .control-group { display: flex; flex-wrap: wrap; gap: 6px; }
      button { border: 1px solid #dfe5ef; border-radius: 9px; background: white; color: #34425c; padding: 8px 11px; font-size: 13px; font-weight: 650; cursor: pointer; }
      button:hover { border-color: #93aef0; background: #f1f5ff; }
      button.primary { color: white; background: #426ff0; border-color: #426ff0; }
      button.primary:hover { background: #315edb; }
      button:disabled { opacity: .48; cursor: default; }
      .panels { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
      .panel { min-width: 0; background: white; border: 1px solid #e8edf5; border-radius: 14px; padding: 10px 12px 8px; overflow: hidden; }
      .panel-heading { display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: 15px; font-weight: 750; padding: 1px 3px 4px; }
      .panel-heading small { color: #8490a5; font-size: 11px; font-weight: 500; }
      canvas { display: block; width: 100%; height: 300px; touch-action: none; cursor: grab; }
      canvas:active { cursor: grabbing; }
      .panel-note { min-height: 20px; text-align: center; color: #707d93; font-size: 12px; padding-bottom: 2px; }
      @media (max-width: 650px) {
        .panels { grid-template-columns: 1fr; }
        canvas { height: 260px; }
        .view-controls { justify-content: center; }
        .panel-heading small { font-size: 10px; }
      }
    </style>
    <script>
      const faces = __FACES__;
      const options = __OPTIONS__;
      const center = {x: 450, y: 300};
      const cameras = {
        solid: {yaw: -0.72, pitch: 0.48},
        net: {yaw: -0.72, pitch: 0.48}
      };
      let foldedCount = 0;
      let foldProgress = 0;
      let animating = false;
      let animationDirection = 1;
      let animationFrom = 0;
      let animationTo = 1;
      let animatingStep = 0;
      let autoFold = false;
      let animationStart = 0;
      let lastStepAt = 0;
      const isCurved = Boolean(options.geometry);
      const baseIndex = Math.max(0, faces.findIndex(f => f.name === options.baseFace));
      const foldTree = isCurved ? [] : buildFoldTree(baseIndex);
      const foldOrder = foldTree.slice(1).map(node => node.index);
      const stepCount = isCurved
        ? (options.geometry.type === "cylinder" ? 3 : 2)
        : foldOrder.length;

      function dot(a, b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; }
      function cross(a, b) {
        return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
      }
      function norm(v) { return Math.hypot(v[0], v[1], v[2]) || 1; }
      function add(a, b) { return a.map((value, i) => value + b[i]); }
      function subtract(a, b) { return a.map((value, i) => value - b[i]); }
      function scaleVector(a, amount) { return a.map(value => value * amount); }
      function average(points) {
        return points.reduce((sum, point) => add(sum, point), [0, 0, 0]).map(value => value / points.length);
      }
      function samePoint(a, b) {
        return Math.abs(a[0] - b[0]) < 1e-4 && Math.abs(a[1] - b[1]) < 1e-4;
      }
      function sharedEdges(a, b) {
        const matches = [];
        a.net.forEach((start, edgeA) => {
          const end = a.net[(edgeA + 1) % a.net.length];
          b.net.forEach((otherStart, edgeB) => {
            const otherEnd = b.net[(edgeB + 1) % b.net.length];
            if (samePoint(start, otherEnd) && samePoint(end, otherStart)) {
              matches.push({edgeA, edgeB, reversed: true});
            } else if (samePoint(start, otherStart) && samePoint(end, otherEnd)) {
              matches.push({edgeA, edgeB, reversed: false});
            }
          });
        });
        return matches;
      }
      function buildFoldTree(root) {
        const tree = [{index: root, parent: -1, edgeParent: -1, edgeChild: -1}];
        const visited = new Set([root]);
        for (let cursor = 0; cursor < tree.length; cursor++) {
          const parent = tree[cursor];
          faces.forEach((childFace, childIndex) => {
            if (visited.has(childIndex)) return;
            const edges = sharedEdges(faces[parent.index], childFace);
            if (!edges.length) return;
            const edge = edges[0];
            visited.add(childIndex);
            tree.push({
              index: childIndex,
              parent: parent.index,
              edgeParent: edge.edgeA,
              edgeChild: edge.edgeB
            });
          });
        }
        if (tree.length !== faces.length) {
          throw new Error("전개도의 모든 면이 연결되어 있지 않습니다.");
        }
        return tree;
      }
      function mapFaceToTarget(face, point) {
        const p0 = face.net[0], p1 = face.net[1], p2 = face.net[2];
        const t0 = face.target[0], t1 = face.target[1], t2 = face.target[2];
        const ux = p1[0] - p0[0], uy = p1[1] - p0[1];
        const vx = p2[0] - p0[0], vy = p2[1] - p0[1];
        const determinant = ux * vy - uy * vx;
        const dx = point[0] - p0[0], dy = point[1] - p0[1];
        const a = (dx * vy - dy * vx) / determinant;
        const b = (ux * dy - uy * dx) / determinant;
        return add(t0, add(scaleVector(subtract(t1, t0), a), scaleVector(subtract(t2, t0), b)));
      }
      function rotateAroundAxis(point, start, end, angle) {
        const axis = scaleVector(subtract(end, start), 1 / norm(subtract(end, start)));
        const relative = subtract(point, start);
        const cosine = Math.cos(angle), sine = Math.sin(angle);
        return add(start, add(
          add(scaleVector(relative, cosine), scaleVector(cross(axis, relative), sine)),
          scaleVector(axis, dot(axis, relative) * (1 - cosine))
        ));
      }
      function foldAngle(parentPose, node) {
        const parentFace = faces[node.parent];
        const childFace = faces[node.index];
        const a = parentFace.net[node.edgeParent];
        const b = parentFace.net[(node.edgeParent + 1) % parentFace.net.length];
        const start = parentPose(a), end = parentPose(b);
        const axis = scaleVector(subtract(end, start), 1 / norm(subtract(end, start)));
        const hingeMidpoint = scaleVector(add(start, end), 0.5);
        const sourceCenter = parentPose(average(childFace.net.map(point => [point[0], point[1], 0])).slice(0, 2));
        const targetCenter = average(childFace.target);
        let sourceRadial = subtract(sourceCenter, hingeMidpoint);
        let targetRadial = subtract(targetCenter, hingeMidpoint);
        sourceRadial = subtract(sourceRadial, scaleVector(axis, dot(sourceRadial, axis)));
        targetRadial = subtract(targetRadial, scaleVector(axis, dot(targetRadial, axis)));
        const cosine = Math.max(-1, Math.min(1, dot(sourceRadial, targetRadial) / (norm(sourceRadial) * norm(targetRadial))));
        const sine = dot(axis, cross(sourceRadial, targetRadial)) / (norm(sourceRadial) * norm(targetRadial));
        return Math.atan2(sine, cosine);
      }
      function makeFoldPoses(progressByFace) {
        const fullPoses = [];
        const angles = [];
        const baseFace = faces[baseIndex];
        fullPoses[baseIndex] = point => mapFaceToTarget(baseFace, point);
        foldTree.slice(1).forEach(node => {
          const parentPose = fullPoses[node.parent];
          const angle = foldAngle(parentPose, node);
          const parentFace = faces[node.parent];
          const start = parentPose(parentFace.net[node.edgeParent]);
          const end = parentPose(parentFace.net[(node.edgeParent + 1) % parentFace.net.length]);
          angles[node.index] = angle;
          fullPoses[node.index] = point => rotateAroundAxis(parentPose(point), start, end, angle);
        });

        const poses = [];
        poses[baseIndex] = fullPoses[baseIndex];
        foldTree.slice(1).forEach(node => {
          const parentPose = poses[node.parent];
          const parentFace = faces[node.parent];
          const start = parentPose(parentFace.net[node.edgeParent]);
          const end = parentPose(parentFace.net[(node.edgeParent + 1) % parentFace.net.length]);
          const angle = angles[node.index] * progressByFace[node.index];
          poses[node.index] = point => rotateAroundAxis(parentPose(point), start, end, angle);
        });
        return poses;
      }
      function foldProgressFor(index) {
        if (animating && !isCurved && index === foldOrder[animatingStep]) return foldProgress;
        if (index === baseIndex) return 1;
        const position = foldOrder.indexOf(index);
        if (position < foldedCount) return 1;
        return 0;
      }
      function stepProgressAt(step) {
        if (animating && animatingStep === step) return foldProgress;
        return step < foldedCount ? 1 : 0;
      }
      function project(point, camera, scale, origin) {
        origin = origin || [0, 0, 0];
        point = subtract(point, origin);
        const cy = Math.cos(camera.yaw), sy = Math.sin(camera.yaw);
        const cp = Math.cos(camera.pitch), sp = Math.sin(camera.pitch);
        const x1 = point[0]*cy - point[1]*sy;
        const y1 = point[0]*sy + point[1]*cy;
        const screenY = y1*sp + point[2]*cp;
        const depth = y1*cp - point[2]*sp;
        return [center.x + x1*scale, center.y - screenY*scale, depth];
      }
      function draw(kind) {
        const canvas = document.getElementById(kind === "solid" ? "solidCanvas" : "netCanvas");
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fbfcff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const camera = cameras[kind];
        const progressByFace = faces.map((_, index) => foldProgressFor(index));
        const foldPoses = makeFoldPoses(progressByFace);
        const items = [];
        const allPoints = [];
        let maxExtent = 0;
        faces.forEach((face, index) => {
          if (kind === "net" && options.fault === "missing" && !options.fixed && index === faces.length - 1) return;
          const progress = kind === "solid" ? 1 : progressByFace[index];
          let points = kind === "solid"
            ? face.target
            : face.net.map(point => foldPoses[index]([point[0], point[1], 0]));
          if (kind === "net" && options.fault === "overlap" && !options.fixed && index === faces.length - 1 && progress < 0.01) {
            const centerOfFace = average(points);
            const centerOfFirst = average(faces[0].net.map(point => foldPoses[0]([point[0], point[1], 0])));
            points = points.map(point => add(point, subtract(centerOfFirst, centerOfFace)));
          }
          points.forEach(p => allPoints.push(p));
          points.forEach(p => { maxExtent = Math.max(maxExtent, Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2])); });
          const projected = points.map(p => project(p, camera, 1));
          const averageDepth = projected.reduce((sum, p) => sum + p[2], 0) / projected.length;
          items.push({face, index, progress, points, projected, averageDepth});
        });
        const origin = average(allPoints);
        const scale = kind === "solid"
          ? Math.min(145, 245 / Math.max(1.7, maxExtent))
          : Math.min(106, 250 / Math.max(2.5, maxExtent));
        items.sort((a, b) => a.averageDepth - b.averageDepth);
        items.forEach(item => {
          const points = item.points.map(p => project(p, camera, scale, origin));
          ctx.beginPath();
          points.forEach((p, i) => i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]));
          ctx.closePath();
          const alpha = item.progress > 0.02 ? 0.91 : 0.77;
          ctx.fillStyle = item.face.color;
          ctx.globalAlpha = alpha;
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.lineWidth = item.face.name === options.baseFace ? 4 : 2;
          ctx.strokeStyle = item.face.name === options.baseFace ? "#20345d" : "#ffffff";
          ctx.stroke();
          const cx = points.reduce((sum, p) => sum + p[0], 0) / points.length;
          const cy = points.reduce((sum, p) => sum + p[1], 0) / points.length;
          if (kind === "net" || item.progress > 0.7) {
            ctx.fillStyle = "#17233b";
            ctx.font = "600 15px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(item.face.name, cx, cy);
          }
        });
        if (kind === "net" && options.fault === "overlap" && !options.fixed) {
          ctx.fillStyle = "#b34040";
          ctx.font = "700 14px sans-serif";
          ctx.textAlign = "center";
          ctx.fillText("두 면이 겹쳐 있어요", center.x, 560);
        }
      }
      function drawAll() {
        if (isCurved) {
          drawCurved("net");
          if (options.foldedReveal) drawCurved("solid");
          return;
        }
        draw("net");
        if (options.foldedReveal) draw("solid");
      }
      function cylinderSidePoint(u, v, progress) {
        const {radius, height} = options.geometry;
        if (progress < 0.001) return [(u - 0.5) * 2 * Math.PI * radius, (v - 0.5) * height, 0];
        const angle = 2 * Math.PI * progress * (u - 0.5);
        const rollingRadius = radius / progress;
        return [
          rollingRadius * Math.sin(angle),
          rollingRadius * (1 - Math.cos(angle)) - radius,
          (v - 0.5) * height
        ];
      }
      function coneSidePoint(u, v, progress) {
        const {radius, slant, height} = options.geometry;
        const sectorAngle = 2 * Math.PI * radius / slant;
        const flatAngle = sectorAngle * (u - 0.5);
        const distance = slant * v;
        const flat = [distance * Math.sin(flatAngle), distance * Math.cos(flatAngle), 0];
        const angle = 2 * Math.PI * (u - 0.5);
        const rolled = [radius * v * Math.sin(angle), radius * v * Math.cos(angle), height * v];
        return flat.map((value, i) => value * (1 - progress) + rolled[i] * progress);
      }
      function circlePoint(centerPoint, angle, radius) {
        return [centerPoint[0] + radius * Math.cos(angle), centerPoint[1] + radius * Math.sin(angle), centerPoint[2]];
      }
      function drawCurved(kind) {
        const canvas = document.getElementById(kind === "solid" ? "solidCanvas" : "netCanvas");
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fbfcff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const {type, radius, height, slant} = options.geometry;
        const camera = cameras[kind];
        const solid = kind === "solid";
        const polygons = [];
        const allPoints = [];
        const addPolygon = (points, color) => {
          polygons.push({points, color});
          points.forEach(point => allPoints.push(point));
        };
        const aroundSegments = 48;
        const sideProgress = solid ? 1 : stepProgressAt(0);

        if (type === "cylinder") {
          const verticalSegments = 5;
          for (let i = 0; i < aroundSegments; i++) {
            for (let j = 0; j < verticalSegments; j++) {
              const u0 = i / aroundSegments, u1 = (i + 1) / aroundSegments;
              const v0 = j / verticalSegments, v1 = (j + 1) / verticalSegments;
              addPolygon([
                cylinderSidePoint(u0, v0, sideProgress),
                cylinderSidePoint(u1, v0, sideProgress),
                cylinderSidePoint(u1, v1, sideProgress),
                cylinderSidePoint(u0, v1, sideProgress)
              ], i % 2 ? "#5389ef" : "#6b9af5");
            }
          }
          const capInfo = [
            {step: 1, z: height / 2, netY: height / 2 + radius + 0.4, color: "#f7a94b"},
            {step: 2, z: -height / 2, netY: -height / 2 - radius - 0.4, color: "#37b99a"}
          ];
          capInfo.forEach(cap => {
            const progress = solid ? 1 : stepProgressAt(cap.step);
            const points = [];
            for (let i = 0; i < aroundSegments; i++) {
              const angle = 2 * Math.PI * i / aroundSegments;
              const flat = circlePoint([0, cap.netY, 0], angle, radius);
              const rolled = [radius * Math.sin(angle - Math.PI), -radius * Math.cos(angle - Math.PI), cap.z];
              points.push(flat.map((value, axis) => value * (1 - progress) + rolled[axis] * progress));
            }
            addPolygon(points, cap.color);
          });
        } else {
          const radialSegments = 14;
          const slantHeight = slant;
          for (let i = 0; i < aroundSegments; i++) {
            for (let j = 0; j < radialSegments; j++) {
              const u0 = i / aroundSegments, u1 = (i + 1) / aroundSegments;
              const v0 = j / radialSegments, v1 = (j + 1) / radialSegments;
              addPolygon([
                coneSidePoint(u0, v0, sideProgress),
                coneSidePoint(u1, v0, sideProgress),
                coneSidePoint(u1, v1, sideProgress),
                coneSidePoint(u0, v1, sideProgress)
              ], i % 2 ? "#6386eb" : "#7999f3");
            }
          }
          const baseProgress = solid ? 1 : stepProgressAt(1);
          const netCenter = [0, -slantHeight - radius - 0.45, 0];
          const points = [];
          for (let i = 0; i < aroundSegments; i++) {
            const angle = 2 * Math.PI * i / aroundSegments;
            const flat = circlePoint(netCenter, angle, radius);
            const target = [radius * Math.cos(angle), radius * Math.sin(angle), 0];
            points.push(flat.map((value, axis) => value * (1 - baseProgress) + target[axis] * baseProgress));
          }
          addPolygon(points, "#f7a94b");
        }

        const origin = average(allPoints);
        const scale = solid ? 150 : 63;
        const projected = polygons.map(polygon => ({
          points: polygon.points.map(point => project(point, camera, scale, origin)),
          color: polygon.color
        }));
        projected.sort((a, b) =>
          a.points.reduce((sum, point) => sum + point[2], 0) / a.points.length
          - b.points.reduce((sum, point) => sum + point[2], 0) / b.points.length
        );
        projected.forEach(polygon => {
          ctx.beginPath();
          polygon.points.forEach((point, index) =>
            index === 0 ? ctx.moveTo(point[0], point[1]) : ctx.lineTo(point[0], point[1])
          );
          ctx.closePath();
          ctx.fillStyle = polygon.color;
          ctx.fill();
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 1.2;
          ctx.stroke();
        });
      }
      function angleForNode(targetIndex) {
        const poses = [];
        poses[baseIndex] = point => mapFaceToTarget(faces[baseIndex], point);
        for (const node of foldTree.slice(1)) {
          const parentPose = poses[node.parent];
          const angle = foldAngle(parentPose, node);
          if (node.index === targetIndex) return Math.round(Math.abs(angle) * 180 / Math.PI);
          const parentFace = faces[node.parent];
          const start = parentPose(parentFace.net[node.edgeParent]);
          const end = parentPose(parentFace.net[(node.edgeParent + 1) % parentFace.net.length]);
          poses[node.index] = point => rotateAroundAxis(parentPose(point), start, end, angle);
        }
        return 90;
      }
      function updateStepNote() {
        if (!netNote || (options.fault && !options.fixed)) return;
        if (foldedCount >= stepCount && !animating) {
          netNote.textContent = "완성! 전개도의 면이 모두 제자리에 모였어요.";
          return;
        }
        const step = animating ? animatingStep : foldedCount;
        if (isCurved) {
          if (options.geometry.type === "cylinder") {
            const notes = [
              "1단계: 직사각형을 둥글게 말아요. 가로 길이는 밑면 원의 둘레(2πr)와 같아요.",
              "2단계: 위쪽 원을 원기둥의 윗면에 붙여요.",
              "3단계: 아래쪽 원을 밑면에 붙여 원기둥을 완성해요."
            ];
            netNote.textContent = notes[step] + " (" + foldedCount + " / " + stepCount + "단계 완료)";
          } else {
            const notes = [
              "1단계: 부채꼴을 말아 양쪽 모선을 맞춰요. 호의 길이는 밑면 원둘레, 반지름은 옆선 길이예요.",
              "2단계: 원을 붙여 원뿔의 밑면을 닫아요."
            ];
            netNote.textContent = notes[step] + " (" + foldedCount + " / " + stepCount + "단계 완료)";
          }
          return;
        }
        const node = foldTree.find(item => item.index === foldOrder[step]);
        const angle = node ? angleForNode(node.index) : 0;
        const message = node
          ? (step + 1) + "단계: " + faces[node.index].name + "을(를) " + faces[node.parent].name
            + "과 만나는 변을 축으로 안쪽으로 " + angle + "° 접어요."
          : "기준 면 " + options.baseFace + "은 움직이지 않아요.";
        netNote.textContent = message + " (" + foldedCount + " / " + stepCount + "단계 완료)";
      }
      function resetCamera() {
        cameras.solid = {yaw: -0.72, pitch: 0.48};
        cameras.net = {yaw: -0.72, pitch: 0.48};
      }
      function animate(now) {
        if (animating) {
          const t = Math.min(1, (now - animationStart) / 720);
          const eased = t*t*(3-2*t);
          foldProgress = animationFrom + (animationTo - animationFrom) * eased;
          if (t >= 1) {
            foldedCount = animationDirection > 0 ? animatingStep + 1 : animatingStep;
            foldProgress = 0;
            animating = false;
            lastStepAt = now;
          }
        }
        if (autoFold && !animating && foldedCount < stepCount && now - lastStepAt > 280) {
          startNext();
        }
        updateStepNote();
        drawAll();
        requestAnimationFrame(animate);
      }
      function startNext() {
        if (foldedCount >= stepCount || animating) {
          if (foldedCount >= stepCount) autoFold = false;
          return;
        }
        animatingStep = foldedCount;
        animationDirection = 1;
        animationFrom = 0;
        animationTo = 1;
        foldProgress = 0;
        animationStart = performance.now();
        animating = true;
      }
      function startPrevious() {
        autoFold = false;
        if (animating) {
          animating = false;
          foldProgress = 0;
        }
        if (foldedCount <= 0) return;
        animatingStep = foldedCount - 1;
        animationDirection = -1;
        animationFrom = 1;
        animationTo = 0;
        foldProgress = 1;
        animationStart = performance.now();
        animating = true;
      }
      document.getElementById("topView").onclick = () => {
        cameras.solid.pitch = cameras.net.pitch = Math.PI / 2;
        cameras.solid.yaw = cameras.net.yaw = 0;
      };
      document.getElementById("frontView").onclick = () => {
        cameras.solid.pitch = cameras.net.pitch = 0;
        cameras.solid.yaw = cameras.net.yaw = 0;
      };
      document.getElementById("resetView").onclick = resetCamera;
      document.getElementById("foldPrev").onclick = startPrevious;
      document.getElementById("foldNext").onclick = () => { autoFold = false; startNext(); };
      document.getElementById("foldAuto").onclick = () => { autoFold = true; startNext(); };
      document.getElementById("unfold").onclick = () => {
        autoFold = false; animating = false; foldedCount = 0; foldProgress = 0; resetCamera();
      };
      ["solid", "net"].forEach(kind => {
        const canvas = document.getElementById(kind === "solid" ? "solidCanvas" : "netCanvas");
        let drag = null;
        canvas.addEventListener("pointerdown", event => {
          drag = {x: event.clientX, y: event.clientY};
          canvas.setPointerCapture(event.pointerId);
        });
        canvas.addEventListener("pointermove", event => {
          if (!drag) return;
          const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
          cameras[kind].yaw += dx * 0.009;
          cameras[kind].pitch = Math.max(-Math.PI/2, Math.min(Math.PI/2, cameras[kind].pitch - dy * 0.009));
          drag = {x: event.clientX, y: event.clientY};
        });
        canvas.addEventListener("pointerup", () => { drag = null; });
        canvas.addEventListener("pointercancel", () => { drag = null; });
      });
      if (!options.foldedReveal) {
        const solidCanvas = document.getElementById("solidCanvas");
        solidCanvas.style.display = "none";
        const placeholder = document.createElement("div");
        placeholder.style.cssText = "height:300px;display:grid;place-items:center;text-align:center;color:#71809a;padding:20px";
        placeholder.innerHTML = "먼저 전개도를 보고 도형을 예상해 보세요.<br>정답을 확인하면 입체도형이 나타나요.";
        solidCanvas.parentElement.insertBefore(placeholder, solidCanvas.nextSibling);
      } else {
        document.getElementById("solidNote").textContent = options.shapeName + " · 선택한 기준 면: " + options.baseFace;
      }
      const netNote = document.getElementById("netNote");
      if (options.mode === "net") {
        netNote.textContent = "접힌 면: 0 / " + faces.length + " · 기준 면: " + options.baseFace;
      } else if (options.fault && !options.fixed) {
        netNote.textContent = options.fault === "missing"
          ? "면이 하나 빠진 전개도예요. 어느 면이 필요할까요?"
          : "두 면의 자리가 겹쳐 있어요. 빈자리로 옮겨 보세요.";
      } else {
        netNote.textContent = "접힌 면: 0 / " + faces.length + " · 기준 면: " + options.baseFace;
      }
      const nextButton = document.getElementById("foldNext");
      const foldButton = document.getElementById("foldAuto");
      const previousButton = document.getElementById("foldPrev");
      const unfoldButton = document.getElementById("unfold");
      if (isCurved) nextButton.textContent = "다음 단계";
      updateStepNote();
      if (!options.foldedReveal) {
        nextButton.disabled = foldButton.disabled = previousButton.disabled = unfoldButton.disabled = true;
      }
      requestAnimationFrame(animate);
    </script>
    """
    html = template.replace("__FACES__", shape_json).replace("__OPTIONS__", options_json)
    st.iframe(
        html,
        height=460,
        alt=f"{shape_name} 입체도형과 전개도 인터랙티브 탐구",
    )


st.markdown(
    """
    <style>
      .stApp { background: #f5f7fc; }
      .block-container { max-width: 1240px; padding-top: 2rem; }
      h1, h2, h3 { letter-spacing: -0.035em; }
      div[data-testid="stMetric"] {
        background: white; border: 1px solid #e9edf5; border-radius: 14px;
        padding: 12px 16px;
      }
      .hero {
        background: linear-gradient(115deg, #eaf0ff, #f8f1ff 65%, #e8f7f4);
        border: 1px solid #e2e8f4; border-radius: 20px; padding: 22px 26px;
        margin-bottom: 14px;
      }
      .hero p { color: #61708a; margin: 6px 0 0; }
    </style>
    <div class="hero">
      <h1>🧊 입체도형 탐험실</h1>
      <p>전개도를 돌려 보고, 한 면씩 접어 입체도형의 비밀을 찾아보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "shape_collection" not in st.session_state:
    st.session_state.shape_collection = []

st.sidebar.title("탐험 메뉴")
mode_label = st.sidebar.radio(
    "무엇을 해볼까요?",
    ["도형 탐험", "거꾸로 추리하기", "전개도 고치기"],
    label_visibility="collapsed",
)

fault = ""
fixed = False
folded_reveal = True
checked = False

if mode_label == "거꾸로 추리하기":
    problem = st.sidebar.selectbox("전개도 문제", list(PROBLEMS))
    shape_name = PROBLEMS[problem]
    st.sidebar.caption("입체도형을 보기 전에 전개도의 면 모양과 연결을 살펴보세요.")
    guess = st.sidebar.selectbox("어떤 도형이 될까요?", POLYHEDRON_NAMES, key=f"guess_{problem}")
    if st.sidebar.button("내 추리 확인", type="primary", use_container_width=True):
        st.session_state[f"guess_checked_{problem}"] = guess == shape_name
        st.session_state[f"guess_answered_{problem}"] = True
    checked = st.session_state.get(f"guess_answered_{problem}", False)
    if checked and st.session_state.get(f"guess_checked_{problem}", False):
        st.sidebar.success(f"정답이에요! {shape_name} 전개도입니다.")
    elif checked:
        st.sidebar.info("아직 정답이 아니에요. 다시 살펴보고 한 번 더 추리해 보세요.")
    folded_reveal = checked and st.session_state.get(f"guess_checked_{problem}", False)
    base_face = SHAPES[shape_name]["faces"][0]["name"]
elif mode_label == "전개도 고치기":
    shape_name = st.sidebar.selectbox("도형 고르기", POLYHEDRON_NAMES, key="fix_shape")
    fault_label = st.sidebar.radio(
        "전개도의 오류",
        ["빠진 면 찾기", "겹친 면 옮기기"],
        help="그림에서 면이 부족한지, 두 면이 같은 자리에 있는지 찾아보세요.",
    )
    fault = "missing" if fault_label == "빠진 면 찾기" else "overlap"
    expected_fix = "빠진 면을 추가한다" if fault == "missing" else "겹친 면을 빈자리로 옮긴다"
    fix_answer = st.sidebar.radio(
        "어떻게 고칠까요?",
        ["빠진 면을 추가한다", "겹친 면을 빈자리로 옮긴다"],
        key=f"fix_answer_{shape_name}_{fault}",
    )
    if st.sidebar.button("수정 확인", type="primary", use_container_width=True):
        st.session_state[f"fixed_{shape_name}_{fault}"] = fix_answer == expected_fix
    fixed = st.session_state.get(f"fixed_{shape_name}_{fault}", False)
    if fixed:
        st.sidebar.success("잘 고쳤어요! 이제 모든 면이 제자리에 있어요.")
    else:
        st.sidebar.caption("전개도를 살펴보고 알맞은 수정 방법을 골라 보세요.")
    base_face = SHAPES[shape_name]["faces"][0]["name"]
else:
    shape_name = st.sidebar.selectbox("도형 고르기", SHAPE_NAMES)
    if SHAPES[shape_name].get("geometry"):
        base_face = "옆면의 시작선을 고정"
        st.sidebar.caption("옆면이 말릴 때 시작하는 선을 기준으로 고정해요.")
    else:
        base_face = st.sidebar.selectbox(
            "기준 면",
            [item["name"] for item in SHAPES[shape_name]["faces"]],
            help="기준 면을 바꾸면 그 면을 밑면으로 삼아 입체를 살펴봅니다.",
            key=f"base_{shape_name}",
        )

if mode_label == "도형 탐험":
    st.subheader(shape_name)
    st.write(SHAPES[shape_name]["description"])
    viewer_mode = "solid"
elif mode_label == "거꾸로 추리하기":
    st.subheader(f"{problem}: 전개도로 도형 맞히기")
    st.write("먼저 전개도의 면 개수와 모양을 살펴보세요. 추리를 확인하면 입체도형이 공개됩니다.")
    viewer_mode = "net"
else:
    st.subheader(f"{shape_name}: 잘못된 전개도 고치기")
    st.write("빠진 면이 있는지, 겹친 면이 있는지 찾아서 바르게 고쳐 보세요.")
    viewer_mode = "net"

left, right = st.columns([3, 1], gap="medium")
with left:
    render_viewer(
        shape_name,
        base_face,
        viewer_mode,
        folded_reveal=folded_reveal,
        fault=fault,
        fixed=fixed,
    )
with right:
    st.markdown("#### 도형 한눈에 보기")
    st.metric("면 · 모서리 · 꼭짓점", SHAPES[shape_name]["fact"])
    st.markdown("#### 이번 탐구")
    if mode_label == "도형 탐험":
        st.write("1. 마우스로 입체와 전개도를 각각 돌려 봅니다.")
        st.write("2. **다음 단계**와 **이전 단계**로 접히는 순서를 확인합니다.")
        st.write("3. 위에서 보기와 정면 보기로 모양을 비교합니다.")
        if st.button("이 도형을 내 도감에 기록", type="primary", use_container_width=True):
            entry = {"shape": shape_name, "base": base_face, "fact": SHAPES[shape_name]["fact"]}
            if entry not in st.session_state.shape_collection:
                st.session_state.shape_collection.append(entry)
                st.toast(f"{shape_name}을(를) 도감에 기록했어요!")
            else:
                st.info("이 도형과 기준 면은 이미 도감에 있어요.")
    elif mode_label == "거꾸로 추리하기":
        st.write("1. 전개도의 면 모양과 연결된 변을 살펴봅니다.")
        st.write("2. 왼쪽 메뉴에서 입체도형을 먼저 예상합니다.")
        st.write("3. 정답 확인 후 입체와 전개도를 비교합니다.")
    else:
        st.write("1. 전개도에 보이지 않는 면이 있는지 찾아봅니다.")
        st.write("2. 또는 면들이 서로 겹치는 자리가 있는지 확인합니다.")
        st.write("3. 알맞은 수정 방법을 골라 확인합니다.")

with st.expander(f"📚 내 도형 도감 ({len(st.session_state.shape_collection)})", expanded=bool(st.session_state.shape_collection)):
    if st.session_state.shape_collection:
        cards = st.columns(min(3, len(st.session_state.shape_collection)))
        for index, entry in enumerate(st.session_state.shape_collection):
            with cards[index % len(cards)]:
                st.markdown(f"**{entry['shape']}**")
                st.caption(f"기준 면: {entry['base']}")
                st.caption(entry["fact"])
    else:
        st.caption("도형 탐험에서 기록 버튼을 누르면 이곳에 나만의 도감이 쌓여요.")
