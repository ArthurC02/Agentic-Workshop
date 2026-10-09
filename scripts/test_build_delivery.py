"""Pedagogical boundary regressions: do not pre-answer B0 or remove analysis clues."""
import copy
import io
import json
import unittest
import zipfile
from build_delivery import ROOT, MANIFEST, B0_ROOT, B0_CONTEXT_FILES, content_policy, destination_check, digest
from verify_delivery import inspect_zip


class B0PackagingPolicyTests(unittest.TestCase):
    def setUp(self):
        self.package=next(p for p in json.loads(MANIFEST.read_text(encoding='utf-8'))['packages'] if p['id']=='participant-29-b0')
        self.payload={e['destination']:(ROOT/e['source']).read_bytes() for e in self.package['files']}
        self.payload.update({name:body.encode('utf-8') for name,body in self.package['generated'].items()})

    def zip_bytes(self,payload):
        expected={**self.package,'files':{name:digest(data) for name,data in payload.items()}}
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as archive:
            for name,data in payload.items():archive.writestr(name,data)
            archive.writestr('PACKAGE-MANIFEST.json',json.dumps({'files':expected['files']}))
        return stream.getvalue(),expected

    def test_safe_baseline_preserves_public_rule_and_original_clues(self):
        content_policy(self.package,self.payload)
        self.assertIn('75%',self.payload[B0_ROOT+'/docs/context.md'].decode('utf-8'))
        data,expected=self.zip_bytes(self.payload)
        self.assertEqual(inspect_zip(data,expected),self.payload)

    def test_missing_each_controlled_document_or_adr_fails_even_with_updated_zip_hashes(self):
        for name in B0_CONTEXT_FILES:
            with self.subTest(name=name):
                altered=dict(self.payload)
                altered.pop(B0_ROOT+'/'+name)
                with self.assertRaisesRegex(ValueError,'Missing controlled B0 context'):content_policy(self.package,altered)
                data,expected=self.zip_bytes(altered)
                with self.assertRaisesRegex(ValueError,'Missing controlled B0 context'):inspect_zip(data,expected)

    def test_reintroduced_diagnosis_and_priority_fail_in_prepared_files_and_actual_zip(self):
        for leak in ('B0保留受控學生票Bug。','學生票錯誤率85%。','BUG-B0-001','優惠先匹配企業、提前、學生。','CORP→ADV→STUDENT'):
            with self.subTest(leak=leak):
                altered=dict(self.payload)
                altered[B0_ROOT+'/docs/context.md']+=('\n'+leak).encode('utf-8')
                with self.assertRaisesRegex(ValueError,'discloses'):content_policy(self.package,altered)
                data,expected=self.zip_bytes(altered)
                with self.assertRaisesRegex(ValueError,'discloses'):inspect_zip(data,expected)

    def test_modified_controlled_context_rejected(self):
        for name in B0_CONTEXT_FILES:
            altered=dict(self.payload)
            altered[B0_ROOT+'/'+name]+=b' altered'
            with self.assertRaisesRegex(ValueError,'original bytes'):content_policy(self.package,altered)

    def test_answer_in_other_markdown_file_is_also_rejected(self):
        for leak in ('學生票錯誤率85%。','CORP→ADV→STUDENT'):
            altered=dict(self.payload)
            altered[B0_ROOT+'/docs/unreviewed-note.md']=leak.encode('utf-8')
            with self.assertRaisesRegex(ValueError,'discloses'):content_policy(self.package,altered)
            data,expected=self.zip_bytes(altered)
            with self.assertRaisesRegex(ValueError,'discloses'):inspect_zip(data,expected)

    def test_adr_exception_is_exact_b0_only(self):
        for name in B0_CONTEXT_FILES[2:]:
            self.assertEqual(destination_check(self.package,B0_ROOT+'/'+name),B0_ROOT+'/'+name)
        for package in ({'id':'recovery-52-b1','role':'participant'},{'id':'recovery-63-b2','role':'participant'}):
            with self.assertRaisesRegex(ValueError,'Role violation'):destination_check(package,B0_ROOT+'/'+B0_CONTEXT_FILES[2])
        with self.assertRaisesRegex(ValueError,'Role violation'):destination_check(self.package,B0_ROOT+'/docs/adr/future-answer.md')

    def test_recovery_ships_context_docs_and_b1_hides_b2_rules(self):
        packages={p['id']:p for p in json.loads(MANIFEST.read_text(encoding='utf-8'))['packages']}
        for pid,root,extra in (('recovery-52-b1','recovery-b1',()),('recovery-63-b2','recovery-b2',('docs/api-examples.md',))):
            package=packages[pid]
            destinations={e['destination'] for e in package['files']}
            for name in (*B0_CONTEXT_FILES,*extra):self.assertIn(root+'/'+name,destinations)
            for name in destinations:destination_check(package,name)
            with self.assertRaisesRegex(ValueError,'Role violation'):destination_check(package,root+'/docs/adr/future-answer.md')
            payload={e['destination']:(ROOT/e['source']).read_bytes() for e in package['files']}
            payload.update({name:body.encode('utf-8') for name,body in package['generated'].items()})
            content_policy(package,payload)
        with self.assertRaisesRegex(ValueError,'discloses B2'):content_policy(packages['recovery-52-b1'],{'recovery-b1/docs/x.md':'FARE-007'.encode()})


if __name__=='__main__':unittest.main()
