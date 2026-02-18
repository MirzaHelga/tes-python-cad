import ezdxf
import trimesh
import math

class CadEngineer:
    def __init__(self):
        print("\n" + "="*40)
        print("    CAD GENERATOR PRO (CHAIR & ROOM)    ")
        print("="*40)

    # HELPER: GAMBAR KOTAK 2D
    def draw_rect_manual(self, msp, x, y, w, h, color):
        points = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        msp.add_lwpolyline(points, close=True, dxfattribs={'color': color})

    # CORE MATH: 3D -> 2D ISOMETRIC
    def get_iso_local(self, x, y, z):
        angle = math.radians(30)
        u = (x - y) * math.cos(angle)
        v = z + (x + y) * math.sin(angle)
        return u, v

    def draw_iso_box(self, msp, layout_offset, local_pos, size, color=4):
        lx, ly = layout_offset
        dx, dy, dz = local_pos
        w, l, h = size
        
        def get_pt(loc_x, loc_y, loc_z):
            u, v = self.get_iso_local(dx + loc_x, dy + loc_y, dz + loc_z)
            return (lx + u, ly + v)

        p0 = get_pt(0, 0, 0); p1 = get_pt(w, 0, 0); p2 = get_pt(w, l, 0); p3 = get_pt(0, l, 0)
        p4 = get_pt(0, 0, h); p5 = get_pt(w, 0, h); p6 = get_pt(w, l, h); p7 = get_pt(0, l, h)

        msp.add_lwpolyline([p0, p1, p2, p3], close=True, dxfattribs={'color': color}) 
        msp.add_lwpolyline([p4, p5, p6, p7], close=True, dxfattribs={'color': color}) 
        for s, e in [(p0,p4), (p1,p5), (p2,p6), (p3,p7)]:
            msp.add_line(s, e, dxfattribs={'color': color})

    # MAIN LOGIC: DXF GENERATOR
    def generate_dxf(self, data, nama_file):
        print(f"[Proses] Membuat DXF: {nama_file}...")
        doc = ezdxf.new()
        msp = doc.modelspace()
        
        w, l, h = data['lebar'], data['panjang'], data['tinggi']
        tipe = data['tipe']
        gap = 100 
        
        y_front = l + gap 
        iso_vis_w = (w + l) * math.cos(math.radians(30))
        
        layout_iso_x = w + gap + (iso_vis_w / 2)
        layout_iso_y = y_front - (l * math.sin(math.radians(30))) 
        iso_off = (layout_iso_x, layout_iso_y)

        if tipe == 'kursi':
            seat_h = h * 0.45; thick = 5
            # 1. TAMPAK ATAS
            self.draw_rect_manual(msp, 0, 0, w, l, 1)
            self.draw_rect_manual(msp, 0, l-thick, w, thick, 1)
            self.draw_rect_manual(msp, 0, 0, thick, thick, 1)
            self.draw_rect_manual(msp, w-thick, 0, thick, thick, 1)
            # 2. TAMPAK DEPAN
            self.draw_rect_manual(msp, 0, y_front, thick, seat_h, 5)
            self.draw_rect_manual(msp, w-thick, y_front, thick, seat_h, 5)
            self.draw_rect_manual(msp, 0, y_front+seat_h, w, thick, 5)
            self.draw_rect_manual(msp, 0, y_front, thick, h, 5)
            self.draw_rect_manual(msp, w-thick, y_front, thick, h, 5)
            self.draw_rect_manual(msp, 0, y_front+h-thick*2, w, thick*2, 5)
            # 3. ISOMETRIK
            self.draw_iso_box(msp, iso_off, (0, 0, 0), (thick, thick, seat_h), 4)
            self.draw_iso_box(msp, iso_off, (w-thick, 0, 0), (thick, thick, seat_h), 4)
            self.draw_iso_box(msp, iso_off, (0, l-thick, 0), (thick, thick, h), 4)
            self.draw_iso_box(msp, iso_off, (w-thick, l-thick, 0), (thick, thick, h), 4)
            self.draw_iso_box(msp, iso_off, (0, 0, seat_h), (w, l, thick), 4)
            self.draw_iso_box(msp, iso_off, (0, l-thick, h-thick*2), (w, thick, thick*2), 4)

        elif tipe == 'ruangan':
            t = 15
            # 1. TAMPAK ATAS (DENAH)
            self.draw_rect_manual(msp, 0, 0, w, l, 1) 
            self.draw_rect_manual(msp, t, t, w-2*t, l-2*t, 1) 
            def draw_denah_opening(side, size, col):
                half = size / 2
                if side == 'barat':
                    msp.add_line((t, l/2-half), (t, l/2+half), dxfattribs={'color': col, 'lineweight': 30})
                    msp.add_line((0, l/2-half), (0, l/2+half), dxfattribs={'color': col, 'lineweight': 30})
                elif side == 'timur':
                    msp.add_line((w-t, l/2-half), (w-t, l/2+half), dxfattribs={'color': col, 'lineweight': 30})
                    msp.add_line((w, l/2-half), (w, l/2+half), dxfattribs={'color': col, 'lineweight': 30})
                elif side == 'utara':
                    msp.add_line((w/2-half, l-t), (w/2+half, l-t), dxfattribs={'color': col, 'lineweight': 30})
                    msp.add_line((w/2-half, l), (w/2+half, l), dxfattribs={'color': col, 'lineweight': 30})
                elif side == 'selatan':
                    msp.add_line((w/2-half, t), (w/2+half, t), dxfattribs={'color': col, 'lineweight': 30})
                    msp.add_line((w/2-half, 0), (w/2+half, 0), dxfattribs={'color': col, 'lineweight': 30})
            if data['p_side'] != 'n': draw_denah_opening(data['p_side'], 90, 3) 
            if data['j_side'] != 'n': draw_denah_opening(data['j_side'], 120, 2) 
            # 2. TAMPAK DEPAN
            self.draw_rect_manual(msp, 0, y_front, w, h, 5)
            # 3. ISOMETRIK
            self.draw_iso_box(msp, iso_off, (0, 0, -5), (w, l, 5), color=8) 
            self.draw_iso_box(msp, iso_off, (0, 0, 0), (w, l, h), color=4) 
            def draw_iso_opening(side, width, height, elev, col):
                if side == 'barat':   self.draw_iso_box(msp, iso_off, (0, l/2-width/2, elev), (t, width, height), col)
                elif side == 'timur': self.draw_iso_box(msp, iso_off, (w-t, l/2-width/2, elev), (t, width, height), col)
                elif side == 'utara': self.draw_iso_box(msp, iso_off, (w/2-width/2, l-t, elev), (width, t, height), col)
                elif side == 'selatan': self.draw_iso_box(msp, iso_off, (w/2-width/2, 0, elev), (width, t, height), col)
            if data['p_side'] != 'n': draw_iso_opening(data['p_side'], 90, 210, 0, 3)
            if data['j_side'] != 'n': draw_iso_opening(data['j_side'], 120, 100, 100, 2)

        msp.add_text("TAMPAK ATAS", dxfattribs={'height': 5}).set_placement((w/2, -15), align=ezdxf.enums.TextEntityAlignment.CENTER)
        msp.add_text("TAMPAK DEPAN", dxfattribs={'height': 5}).set_placement((w/2, y_front-15), align=ezdxf.enums.TextEntityAlignment.CENTER)
        msp.add_text("ISOMETRIC", dxfattribs={'height': 5}).set_placement((layout_iso_x, layout_iso_y - 40), align=ezdxf.enums.TextEntityAlignment.CENTER)
        
        doc.saveas(nama_file)

    #3D LOGIC: STL GENERATOR (WITH HOLES)
    def generate_3d(self, data, nama_file):
        print(f"[Proses] Membuat STL: {nama_file}...")
        w, l, h = data['lebar'], data['panjang'], data['tinggi']
        parts = []
        
        if data['tipe'] == 'kursi':
            thick, seat_h = 5, h * 0.45
            parts.append(trimesh.creation.box([w, l, thick]).apply_translation([0, 0, seat_h]))
            parts.append(trimesh.creation.box([thick, thick, seat_h]).apply_translation([-w/2+thick/2, -l/2+thick/2, seat_h/2]))
            parts.append(trimesh.creation.box([thick, thick, seat_h]).apply_translation([w/2-thick/2, -l/2+thick/2, seat_h/2]))
            parts.append(trimesh.creation.box([thick, thick, h]).apply_translation([-w/2+thick/2, l/2-thick/2, h/2]))
            parts.append(trimesh.creation.box([thick, thick, h]).apply_translation([w/2-thick/2, l/2-thick/2, h/2]))
            parts.append(trimesh.creation.box([w, thick, thick*2]).apply_translation([0, l/2-thick/2, h-thick]))
        
        elif data['tipe'] == 'ruangan':
            t = 15
            def create_wall_with_hole(wall_w, wall_h, hole_side, is_door=False):
                if (is_door and data['p_side'] != hole_side) and (not is_door and data['j_side'] != hole_side):
                    return [trimesh.creation.box([wall_w, t, wall_h])]
                hw, hh, he = (90, 210, 0) if is_door else (120, 100, 100)
                wall_parts = []
                wall_parts.append(trimesh.creation.box([(wall_w-hw)/2, t, wall_h]).apply_translation([-(wall_w+hw)/4, 0, 0]))
                wall_parts.append(trimesh.creation.box([(wall_w-hw)/2, t, wall_h]).apply_translation([(wall_w+hw)/4, 0, 0]))
                wall_parts.append(trimesh.creation.box([hw, t, wall_h-(hh+he)]).apply_translation([0, 0, (hh+he)/2]))
                if not is_door: wall_parts.append(trimesh.creation.box([hw, t, he]).apply_translation([0, 0, -wall_h/2 + he/2]))
                return wall_parts

            for p in create_wall_with_hole(w, h, 'utara', data['p_side']=='utara'): parts.append(p.apply_translation([0, l/2, h/2]))
            for p in create_wall_with_hole(w, h, 'selatan', data['p_side']=='selatan'): parts.append(p.apply_translation([0, -l/2, h/2]))
            for p in create_wall_with_hole(l, h, 'timur', data['p_side']=='timur'): parts.append(p.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [0,0,1])).apply_translation([w/2, 0, h/2]))
            for p in create_wall_with_hole(l, h, 'barat', data['p_side']=='barat'): parts.append(p.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [0,0,1])).apply_translation([-w/2, 0, h/2]))
            
        if parts: trimesh.util.concatenate(parts).export(nama_file)

if __name__ == "__main__":
    app = CadEngineer()
    print("Pilih:\n1. Kursi\n2. Ruangan")
    pil = input(">> ")
    tipe = 'kursi' if pil == '1' else 'ruangan'
    try:
        w = float(input(f"Lebar: ")); l = float(input(f"Panjang: ")); h = float(input(f"Tinggi: "))
        ps, js = 'n', 'n'
        if tipe == 'ruangan':
            ps = input("Sisi Pintu (utara/selatan/barat/timur/n): ").lower()
            js = input("Sisi Jendela (utara/selatan/barat/timur/n): ").lower()
        data = {'tipe': tipe, 'lebar': w, 'panjang': l, 'tinggi': h, 'p_side': ps, 'j_side': js}
        nama = f"{tipe}_{int(w)}x{int(l)}x{int(h)}"
        app.generate_dxf(data, f"{nama}.dxf"); app.generate_3d(data, f"{nama}.stl")
        print(f"\n[SUKSES] Cek file {nama}.dxf & .stl")
    except Exception as e: print(f"Error: {e}")