

    public RegularTimePeriod previous() {
        if (this.year > Year.MINIMUM_YEAR) {
            return new Year(this.year - 1);
        }
        else {
            return null;
        }
    }

  