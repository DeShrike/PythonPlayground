#include <Python.h>
#include <complexobject.h>

// https://stackabuse.com/enhancing-python-with-custom-c-extensions/
// https://docs.python.org/2.0/ext/parseTuple.html

// Function 1: A simple 'hello world' function
static PyObject* helloworld(PyObject* self, PyObject* args)
{
    printf("Hello World\n");
    return Py_None;
}

static PyObject* print_complex(PyObject* self, PyObject* args)
{
    Py_complex c;

    if (!PyArg_ParseTuple(args, "D:print_complex", &c))
    {
        return NULL;
    }

    printf("%f + %f i \n", c.real, c.imag);

    return Py_None;
}

static PyObject* simple_print(PyObject* self, PyObject* args)
{
    char *s1;
    char *s2;
    if (!PyArg_ParseTuple(args, "ss", &s1, &s2))
    {
        return NULL;
    }

    printf(s1);
    printf("\n");
    printf(s2);
    printf("\n");

    return Py_None;
}

// Function 2: Add 2 integers
static PyObject * add(PyObject* self, PyObject* args)
{
    int sum;
    int num1;
    int num2;
    if (!PyArg_ParseTuple(args, "ii", &num1, &num2))
    {
        return NULL;
    }

    sum = num1 + num2;

    return Py_BuildValue("i", sum);
}

int Cfib(int n)
{
    if (n < 2)
    {
        return n;
    }
    else
    {
        return Cfib(n-1) + Cfib(n-2);
    }
}

static PyObject* fib(PyObject* self, PyObject* args)
{
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
    {
        return NULL;
    }

    return Py_BuildValue("i", Cfib(n));
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "helloworld", helloworld, METH_NOARGS,  "Prints Hello World" },
    { "add",        add       , METH_VARARGS, "Add 2 integers" },
    { "simple_print", simple_print, METH_VARARGS, "Print 2 strings" },
    { "print_complex", print_complex, METH_VARARGS, "Print Complex Number" },
    { "fib",          fib, METH_VARARGS, "Calculate the fibonaci numbers"},
    { "version", (PyCFunction)version, METH_NOARGS, "Return the version"},
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "HelloC",
    "Calling C from Python",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_HelloC(void)
{
    return PyModule_Create(&myModule);
}
