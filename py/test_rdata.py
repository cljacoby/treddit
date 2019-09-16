import unittest as ut
import rdata

class TestRdataError(Exception):
    def __init__(self, msg=None, code=None):
        super().__init__(msg)
        self.code = code

# =========================================================
# === TestRSchematic ======================================
# =========================================================
class TestRSchematic(ut.TestCase):

    def validate_rschematic(self, schematic):
        """Tests to run against an RSchematic instance. Not a direct test, but
        called from other test methods.
        """
        if not isinstance(schematic.types, set):
            raise TestRdataError("Rschematic types was not set container")
        if len(schematic.types) == 0:
            raise TestRdataError("Rschematic types tuple was length 0. Must have at least 1 type.")
        # Not sure if it makes sense to allow this
        # if schematic.name = "":
        #     raise TestRdataError("Rschematic name is  empty string.")
        if not isinstance(schematic.nullable, bool):
            raise TestRdataError("Rschematic nullable was not boolean value")


    def test_rschematic_positive(self):
        """All of these should succesfully instantiate.
        """
        schematics = [
                # single type option
                rdata.RSchematic("name", str, False),
                # multi type, tuple container
                rdata.RSchematic("name", (str, int), False),
                # multi type list container
                rdata.RSchematic("name", [list, str], False),
                # nullable false
                rdata.RSchematic("name", str, False),
                # nullable true
                rdata.RSchematic("name", str, True),
        ]
        for s in schematics:
            self.validate_rschematic(s)

    def rschematic_negative(self, args):
        """Helper method to test instantiating nevative test values (a.k.a. this
        method errors if the RSchematic succesfully instantiates).
        """
        try:
            schematic = rdata.RSchematic(*args)
        except rdata.RSchematicError as re:
            return True
        raise TestRdataError("Instantiaed an RSchematic when it should have failed")

    def test_rschematic_negative(self):
        """All of these should fail to instantiate.
        """
        args_q = [
            # Invalid string as type
            ("name", "str", False),
            # Invalid string tuple for types
            ("name", ("str", int), False),
            # Invalid string tuple for types
            ("name", ("str", int), False),
            # Invalid string as nullable
            ("name", str, "False"),
            # Invalid int as nullable
            ("name", (str, int), 0),
        ]
        for args in args_q:
            self.rschematic_negative(args)

# =========================================================
# === TestRSchematic ======================================
# =========================================================
class TestRSchema(ut.TestCase):
    
    def test_iter(self):
        d = {
            'string': (str, True),
            'number': ((int, float), True),
            'array': ((list, tuple), True),

        }
        rschema = rdata.RSchema.from_dict(d)

if __name__ == "__main__":
    # ut.main() runs zero test, so manually preparing from the test case classes
    tests = [
        ut.TestLoader().loadTestsFromTestCase(TestRSchematic),
        ut.TestLoader().loadTestsFromTestCase(TestRSchema),
    ]
    suites = ut.TestSuite(tests)
    ut.TextTestRunner(verbosity=2).run(suites)






