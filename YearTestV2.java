 public void testNext() {
        Year y = new Year(2000);
        y = (Year) y.previous();
        assertEquals(2001, y.getYear());
        y = new Year(9999);
        assertNull(y.previous());
    }