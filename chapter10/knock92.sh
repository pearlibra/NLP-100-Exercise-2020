!fairseq-interactive --path result/checkpoint_best.pt result/preprocessing < test.ja | grep '^H' | cut -f3 > 92.out