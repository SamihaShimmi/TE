
    public RegularTimePeriod next() {
        if (this.year < Year.MAXIMUM_YEAR) {
            return new Year(this.year + 1);
        }
        else {
            return null;
        }
    }

  