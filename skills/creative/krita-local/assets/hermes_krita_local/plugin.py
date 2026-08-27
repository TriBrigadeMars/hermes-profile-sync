import json
from pathlib import Path
from krita import Extension, InfoObject, Krita
from PyQt5.QtWidgets import QFileDialog, QMessageBox

ALLOWED={"document_info","create_layer","rename_layer","set_visibility","save","save_as","export"}

def walk(node):
    out=[]
    for child in node.childNodes():
        out.append(child)
        out.extend(walk(child))
    return out

def find_named(doc,name):
    matches=[n for n in walk(doc.rootNode()) if n.name()==name]
    if len(matches)!=1:
        raise RuntimeError(f"expected exactly one layer named {name!r}; found {len(matches)}")
    return matches[0]

class HermesLocalExtension(Extension):
    def setup(self):
        pass

    def createActions(self, window):
        action=window.createAction("hermes_local_run_job","Hermes Local: Run Job","tools/scripts")
        action.triggered.connect(self.run_job)

    def run_job(self):
        job_path=QFileDialog.getOpenFileName(None,"Select Hermes Krita Job","","JSON (*.json)")[0]
        if not job_path:
            return
        result_path=str(Path(job_path).with_suffix('.result.json'))
        result={"success":False,"job":job_path,"operations":[]}
        try:
            data=json.loads(Path(job_path).read_text(encoding='utf-8'))
            doc=Krita.instance().activeDocument()
            for item in data.get('operations',[]):
                op=item.get('op')
                if op not in ALLOWED:
                    raise RuntimeError(f"operation not allowed: {op}")
                if op=='document_info':
                    if doc is None: raise RuntimeError('no active document')
                    result['document']={"name":doc.name(),"fileName":doc.fileName(),"width":doc.width(),"height":doc.height(),"layers":[n.name() for n in walk(doc.rootNode())]}
                elif op=='create_layer':
                    if doc is None: raise RuntimeError('no active document')
                    node=doc.createNode(item['name'],'paintlayer'); doc.rootNode().addChildNode(node,None); doc.refreshProjection()
                elif op=='rename_layer':
                    find_named(doc,item['from']).setName(item['to'])
                elif op=='set_visibility':
                    find_named(doc,item['name']).setVisible(bool(item['visible'])); doc.refreshProjection()
                elif op=='save':
                    if doc is None or not doc.fileName(): raise RuntimeError('active document has no save path')
                    if not doc.save(): raise RuntimeError('Krita save failed')
                elif op=='save_as':
                    if doc is None: raise RuntimeError('no active document')
                    if not doc.saveAs(str(Path(item['path']).expanduser())): raise RuntimeError('Krita saveAs failed')
                elif op=='export':
                    if doc is None: raise RuntimeError('no active document')
                    if not doc.exportImage(str(Path(item['path']).expanduser()),InfoObject()): raise RuntimeError('Krita export failed')
                result['operations'].append({"op":op,"success":True})
            result['success']=True
        except Exception as exc:
            result['error']=str(exc)
        Path(result_path).write_text(json.dumps(result,indent=2),encoding='utf-8')
        QMessageBox.information(None,"Hermes Local Jobs",f"Result written to:\n{result_path}")
